def calc_fibo_levels(high, low):
    levels = {
        "0.0": high,
        "0.236": high - 0.236 * (high - low),
        "0.382": high - 0.382 * (high - low),
        "0.5": high - 0.5 * (high - low),
        "0.618": high - 0.618 * (high - low),
        "1.0": low
    }
    return levels