def detect_order_blocks(df):
    levels = []
    recent = df.tail(20)
    mean = recent["Close"].mean()
    if recent["Close"].iloc[-1] < mean:
        levels.append({"type": "demand", "level": recent["Low"].min()})
    else:
        levels.append({"type": "supply", "level": recent["High"].max()})
    return levels