import yfinance as yf
import pandas as pd
import ta

def detecter_opportunite(symbole, use_ai=False):
    try:
        df = yf.download(symbole, period="7d", interval="15m", progress=False)
        if df.empty or len(df) < 30:
            return None

        df.dropna(inplace=True)

        # RSI, MACD, EMA
        df["rsi"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
        macd = ta.trend.MACD(df["Close"])
        df["macd"] = macd.macd()
        df["macds"] = macd.macd_signal()
        df["ema9"] = ta.trend.EMAIndicator(df["Close"], 9).ema_indicator()
        df["ema21"] = ta.trend.EMAIndicator(df["Close"], 21).ema_indicator()

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(df["Close"])
        df["boll_upper"] = bb.bollinger_hband()
        df["boll_lower"] = bb.bollinger_lband()
        df["boll_pos"] = (df["Close"] - df["boll_lower"]) / (df["boll_upper"] - df["boll_lower"])

        # Stochastic Oscillator
        stoch = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"])
        df["stoch_k"] = stoch.stoch()

        # PSAR
        df["psar"] = ta.trend.PSARIndicator(df["High"], df["Low"], df["Close"]).psar()
        df["psar_trend"] = df["Close"] > df["psar"]

        last = df.iloc[-1]

        # Logique sniper : conditions très serrées
        score = 0
        if last["rsi"] > 60: score += 1
        if last["macd"] > last["macds"]: score += 1
        if last["ema9"] > last["ema21"]: score += 1
        if last["boll_pos"] < 0.3: score += 1
        if last["stoch_k"] < 20: score += 1
        if last["psar_trend"]: score += 1

        signal = None
        if score >= 5:
            signal = "BUY"
        elif score <= 1:
            signal = "SELL"

        if not signal:
            return None

        return {
            "decision": signal,
            "score": 78,
            "rsi": round(last["rsi"], 2),
            "macd": round(last["macd"], 2),
            "macds": round(last["macds"], 2),
            "ema9": round(last["ema9"], 5),
            "ema21": round(last["ema21"], 5),
            "bollinger_position": round(last["boll_pos"], 3),
            "psar_trend": "up" if last["psar_trend"] else "down",
            "stoch_k": round(last["stoch_k"], 2),
            "sl": 40,
            "tp": 85,
            "context": "sniper"
        }

    except Exception as e:
        print(f"Erreur stratégie Sniper IA : {e}")
        return None