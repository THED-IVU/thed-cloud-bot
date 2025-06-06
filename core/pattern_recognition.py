def detect_patterns(df):
    patterns = []
    if df["Close"].iloc[-1] > df["Open"].iloc[-1] and df["Close"].iloc[-2] < df["Open"].iloc[-2]:
        patterns.append("Engulfing")
    if abs(df["Close"].iloc[-1] - df["Open"].iloc[-1]) < 0.05 * (df["High"].iloc[-1] - df["Low"].iloc[-1]):
        patterns.append("Doji")
    return patterns