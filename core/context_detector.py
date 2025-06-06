def detect_context(df):
    range_ = df["High"].max() - df["Low"].min()
    avg_candle = (df["High"] - df["Low"]).mean()
    last_close = df["Close"].iloc[-1]

    if avg_candle < range_ * 0.2:
        return "range"
    elif df["Close"].iloc[-1] > df["Close"].mean():
        return "tendance_haussière"
    elif df["Close"].iloc[-1] < df["Close"].mean():
        return "tendance_baissière"
    else:
        return "neutre"