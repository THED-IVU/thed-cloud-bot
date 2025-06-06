# core/indicators.py

import pandas as pd
import pandas_ta as ta

# ---------------- INDICATEURS TECHNIQUES ----------------

def calculer_indicateurs(data: pd.DataFrame, params: dict) -> pd.DataFrame:
    rsi_len = params.get("RSI_length", 14)
    macd_fast = params.get("MACD_fast", 12)
    macd_slow = params.get("MACD_slow", 26)
    macd_signal = params.get("MACD_signal", 9)

    # EMA
    data['ema9'] = ta.ema(data['close'], length=9)
    data['ema21'] = ta.ema(data['close'], length=21)

    # Bollinger Bands
    try:
        bb = ta.bbands(data['close'], length=20, std=2)
        if bb is not None:
            data['bbands_l'] = bb['BBL_20_2.0']
            data['bbands_m'] = bb['BBM_20_2.0']
            data['bbands_u'] = bb['BBU_20_2.0']
    except:
        data['bbands_l'] = data['bbands_m'] = data['bbands_u'] = pd.NA

    # RSI
    try:
        data['rsi'] = ta.rsi(data['close'], length=rsi_len)
    except:
        data['rsi'] = pd.NA

    # MACD
    try:
        macd_df = ta.macd(data['close'], fast=macd_fast, slow=macd_slow, signal=macd_signal)
        if macd_df is not None and all(x in macd_df.columns for x in ["MACD_12_26_9", "MACDs_12_26_9"]):
            data["MACD_12_26_9"] = macd_df["MACD_12_26_9"]
            data["MACDs_12_26_9"] = macd_df["MACDs_12_26_9"]
            data["MACDh_12_26_9"] = macd_df.get("MACDh_12_26_9", pd.NA)
        else:
            data["MACD_12_26_9"] = data["MACDs_12_26_9"] = data["MACDh_12_26_9"] = pd.NA
    except:
        data["MACD_12_26_9"] = data["MACDs_12_26_9"] = data["MACDh_12_26_9"] = pd.NA

    # Stochastic
    try:
        stoch = ta.stoch(data['high'], data['low'], data['close'], k=5, d=3)
        if stoch is not None:
            data["STOCHk_5_3_3"] = stoch["STOCHk_5_3_3"]
            data["STOCHd_5_3_3"] = stoch["STOCHd_5_3_3"]
    except:
        data["STOCHk_5_3_3"] = data["STOCHd_5_3_3"] = pd.NA

    # Parabolic SAR
    try:
        psar = ta.psar(data['high'], data['low'], data['close'])
        if psar is not None and "PSARl_0.02_0.2" in psar.columns:
            data['sar'] = psar["PSARl_0.02_0.2"]
    except:
        data['sar'] = pd.NA

    # Fibonacci (50 dernières bougies)
    try:
        max_price = data['high'].rolling(window=50).max()
        min_price = data['low'].rolling(window=50).min()
        data['fibo_38'] = min_price + 0.382 * (max_price - min_price)
        data['fibo_50'] = min_price + 0.500 * (max_price - min_price)
        data['fibo_61'] = min_price + 0.618 * (max_price - min_price)
    except:
        data['fibo_38'] = data['fibo_50'] = data['fibo_61'] = pd.NA

    # Volatilité
    try:
        data['volatilite'] = (data['bbands_u'] - data['bbands_l']) / data['close']
    except:
        data['volatilite'] = pd.NA

    return data

# ---------------- SCORE DE FORCE DE SIGNAL ----------------

def signal_strength(row: pd.Series) -> int:
    strength = 0
    try:
        if row['ema9'] > row['ema21']:
            strength += 1
        elif row['ema9'] < row['ema21']:
            strength -= 1

        if row['rsi'] < 30:
            strength += 1
        elif row['rsi'] > 70:
            strength -= 1

        if row['close'] < row['bbands_l']:
            strength += 1
        elif row['close'] > row['bbands_u']:
            strength -= 1

        if row['MACD_12_26_9'] > row['MACDs_12_26_9']:
            strength += 1
        elif row['MACD_12_26_9'] < row['MACDs_12_26_9']:
            strength -= 1

        if row['STOCHk_5_3_3'] < 20 and row['STOCHk_5_3_3'] > row['STOCHd_5_3_3']:
            strength += 1
        elif row['STOCHk_5_3_3'] > 80 and row['STOCHk_5_3_3'] < row['STOCHd_5_3_3']:
            strength -= 1

        if row['sar'] < row['close']:
            strength += 1
        elif row['sar'] > row['close']:
            strength -= 1

        if row.get('volatilite', 0) > 0.015:
            strength += 1
    except:
        pass

    return strength

# ---------------- WRAPPER UNIVERSEL ----------------

def calculer_tous_les_indicateurs(data: pd.DataFrame, params: dict = None) -> pd.DataFrame:
    if params is None:
        params = {
            "RSI_length": 14,
            "MACD_fast": 12,
            "MACD_slow": 26,
            "MACD_signal": 9
        }
    return calculer_indicateurs(data.copy(), params)
