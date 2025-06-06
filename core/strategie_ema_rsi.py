import yfinance as yf
import pandas as pd
import ta

def detecter_opportunite(symbole, use_ai=False):
    try:
        df = yf.download(symbole, period="7d", interval="15m", progress=False)
        if df.empty or len(df) < 30:
            return None

        df.dropna(inplace=True)
        close = df["Close"]

        # RSI
        df["rsi"] = ta.momentum.RSIIndicator(close).rsi()

        # MACD
        macd = ta.trend.MACD(close)
        df["macd"] = macd.macd()
        df["macds"] = macd.macd_signal()

        # EMA
        df["ema9"] = ta.trend.EMAIndicator(close, window=9).ema_indicator()
        df["ema21"] = ta.trend.EMAIndicator(close, window=21).ema_indicator()

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(close)
        df["boll_upper"] = bb.bollinger_hband()
        df["boll_lower"] = bb.bollinger_lband()
        df["boll_pos"] = (close - df["boll_lower"]) / (df["boll_upper"] - df["boll_lower"])

        # Stochastic Oscillator
        stoch = ta.momentum.StochasticOscillator(df["High"], df["Low"], close)
        df["stoch_k"] = stoch.stoch()

        # Parabolic SAR
        df["psar"] = ta.trend.PSARIndicator(df["High"], df["Low"], close).psar()
        df["psar_trend"] = df["Close"] > df["psar"]

        last = df.iloc[-1]

        signal = None
        if last["ema9"] > last["ema21"] and last["macd"] > last["macds"] and last["rsi"] > 50:
            signal = "BUY"
        elif last["ema9"] < last["ema21"] and last["macd"] < last["macds"] and last["rsi"] < 50:
            signal = "SELL"

        if not signal:
            return None

        result = {
            "decision": signal,
            "score": 75,
            "rsi": round(last["rsi"], 2),
            "macd": round(last["macd"], 2),
            "macds": round(last["macds"], 2),
            "ema9": round(last["ema9"], 5),
            "ema21": round(last["ema21"], 5),
            "bollinger_position": round(last["boll_pos"], 3),
            "psar_trend": "up" if last["psar_trend"] else "down",
            "stoch_k": round(last["stoch_k"], 2),
            "sl": 50,
            "tp": 80,
            "context": "trend",
        }

        return result

    except Exception as e:
        print(f"Erreur stratégie EMA+RSI : {e}")
        return None