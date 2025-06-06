def should_trade(context, pattern, sentiment):
    if context == "range" and pattern == "Engulfing":
        return True
    if sentiment.get("value_classification", "") == "Extreme Fear":
        return False
    return True