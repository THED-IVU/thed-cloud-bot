import yfinance as yf
import pandas as pd
import ta

def detecter_opportunite(symbole, use_ai=False):
    try:
        df = yf.download(symbole, period="7d", interval="15m", progress=False)
        if df.empty or len(df) < 30:
            return None

        df.dropna(inplace=True)
        df["heikin_close"] = (df["Open"] + df["High"] + df["Low"] + df["Close"]) / 4
        df["rsi"] = ta.momentum.RSIIndicator(df["heikin_close"]).rsi()
        macd = ta.trend.MACD(df["heikin_close"])
        df["macd"] = macd.macd()
        df["macds"] = macd.macd_signal()
        df["ema9"] = ta.trend.EMAIndicator(df["heikin_close"], 9).ema_indicator()
        df["ema21"] = ta.trend.EMAIndicator(df["heikin_close"], 21).ema_indicator()

        # Indicateurs supplémentaires
        bb = ta.volatility.BollingerBands(df["heikin_close"])
        df["boll_upper"] = bb.bollinger_hband()
        df["boll_lower"] = bb.bollinger_lband()
        df["boll_pos"] = (df["heikin_close"] - df["boll_lower"]) / (df["boll_upper"] - df["boll_lower"])
        stoch = ta.momentum.StochasticOscillator(df["High"], df["Low"], df["heikin_close"])
        df["stoch_k"] = stoch.stoch()
        df["psar"] = ta.trend.PSARIndicator(df["High"], df["Low"], df["heikin_close"]).psar()
        df["psar_trend"] = df["heikin_close"] > df["psar"]

        last = df.iloc[-1]

        signal = None
        if last["ema9"] > last["ema21"] and last["rsi"] > 50 and last["macd"] > last["macds"]:
            signal = "BUY"
        elif last["ema9"] < last["ema21"] and last["rsi"] < 50 and last["macd"] < last["macds"]:
            signal = "SELL"

        if not signal:
            return None

        return {
            "decision": signal,
            "score": 72,
            "rsi": round(last["rsi"], 2),
            "macd": round(last["macd"], 2),
            "macds": round(last["macds"], 2),
            "ema9": round(last["ema9"], 5),
            "ema21": round(last["ema21"], 5),
            "bollinger_position": round(last["boll_pos"], 3),
            "psar_trend": "up" if last["psar_trend"] else "down",
            "stoch_k": round(last["stoch_k"], 2),
            "sl": 45,
            "tp": 90,
            "context": "trend"
        }

    except Exception as e:
        print(f"Erreur stratégie Heikin+PSAR : {e}")
        return None