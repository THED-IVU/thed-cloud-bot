import yfinance as yf
import pandas as pd
import ta

def detecter_opportunite(symbole, use_ai=False):
    try:
        df = yf.download(symbole, period="7d", interval="15m", progress=False)
        if df.empty or len(df) < 50:
            return None

        df.dropna(inplace=True)

        # Détection de retracement (simplifié)
        recent = df[-30:]
        high = recent["High"].max()
        low = recent["Low"].min()
        close = recent["Close"].iloc[-1]

        niveau_382 = high - 0.382 * (high - low)
        niveau_618 = high - 0.618 * (high - low)

        is_retrace_buy = close < niveau_618 and close > niveau_382

        # Indicateurs techniques
        df["rsi"] = ta.momentum.RSIIndicator(close=df["Close"]).rsi()
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

        # Stochastic
        stoch = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["Close"])
        df["stoch_k"] = stoch.stoch()

        # PSAR
        df["psar"] = ta.trend.PSARIndicator(df["High"], df["Low"], df["Close"]).psar()
        df["psar_trend"] = df["Close"] > df["psar"]

        last = df.iloc[-1]

        signal = None
        if is_retrace_buy and last["rsi"] > 45 and last["macd"] > last["macds"] and last["ema9"] > last["ema21"]:
            signal = "BUY"
        elif not is_retrace_buy and last["rsi"] < 55 and last["macd"] < last["macds"] and last["ema9"] < last["ema21"]:
            signal = "SELL"

        if not signal:
            return None

        return {
            "decision": signal,
            "score": 73,
            "rsi": round(last["rsi"], 2),
            "macd": round(last["macd"], 2),
            "macds": round(last["macds"], 2),
            "ema9": round(last["ema9"], 5),
            "ema21": round(last["ema21"], 5),
            "bollinger_position": round(last["boll_pos"], 3),
            "psar_trend": "up" if last["psar_trend"] else "down",
            "stoch_k": round(last["stoch_k"], 2),
            "sl": 48,
            "tp": 95,
            "context": "retracement"
        }

    except Exception as e:
        print(f"Erreur stratégie Fibo+Bougies : {e}")
        return None