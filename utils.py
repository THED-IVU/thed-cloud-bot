# 📁 utils.py
import pandas as pd
import pandas_ta as ta


# ----------------- INDICATEURS TECHNIQUES -----------------
def calculer_indicateurs(data, params=None):
    if params is None:
        params = {
            'RSI_length': 14,
            'MACD_fast': 12,
            'MACD_slow': 26
        }

    # EMA
    data['EMA_9'] = ta.ema(data['close'], length=9)
    data['EMA_21'] = ta.ema(data['close'], length=21)

    # Bollinger Bands
    bb = ta.bbands(data['close'], length=20, std=2)
    data['BB_lower'] = bb['BBL_20_2.0']
    data['BB_upper'] = bb['BBU_20_2.0']

    # RSI
    data['RSI'] = ta.rsi(data['close'], length=params['RSI_length'])

    # MACD
    macd = ta.macd(data['close'], fast=params['MACD_fast'], slow=params['MACD_slow'])
    data['MACD'] = macd['MACD_12_26_9']
    data['MACD_signal'] = macd['MACDs_12_26_9']

    # Stochastique
    stoch = ta.stoch(data['high'], data['low'], data['close'], k=5, d=3)
    data['StochK'] = stoch['STOCHk_14_3_3']
    data['StochD'] = stoch['STOCHd_14_3_3']

    # Parabolic SAR
    data['SAR'] = ta.sar(data['high'], data['low'])

    # Niveaux de Fibonacci (approx. intra-day)
    high = data['high'].max()
    low = data['low'].min()
    diff = high - low
    data['FIB_38'] = high - 0.382 * diff
    data['FIB_50'] = high - 0.5 * diff
    data['FIB_61'] = high - 0.618 * diff

    return data

# ----------------- GÉNÉRATION DES SIGNAUX -----------------
def generer_signaux_combines(data, params=None):
    data['Signal'] = ''

    for i in range(1, len(data)):
        row = data.iloc[i]
        prev = data.iloc[i - 1]

        # --- Conditions d'achat ---
        achat_ema = row['EMA_9'] > row['EMA_21']
        achat_rsi = row['RSI'] > 50
        achat_macd = row['MACD'] > row['MACD_signal']
        achat_stoch = prev['StochK'] < prev['StochD'] and row['StochK'] > row['StochD'] and row['StochK'] < 20
        achat_sar = row['SAR'] < row['close']
        achat_fib = row['close'] >= row['FIB_38'] and row['close'] <= row['FIB_50']

        if all([achat_ema, achat_rsi, achat_macd, achat_stoch, achat_sar, achat_fib]):
            data.at[data.index[i], 'Signal'] = 'Achat'

        # --- Conditions de vente ---
        vente_ema = row['EMA_9'] < row['EMA_21']
        vente_rsi = row['RSI'] < 50
        vente_macd = row['MACD'] < row['MACD_signal']
        vente_stoch = prev['StochK'] > prev['StochD'] and row['StochK'] < row['StochD'] and row['StochK'] > 80
        vente_sar = row['SAR'] > row['close']
        vente_fib = row['close'] <= row['FIB_61'] and row['close'] >= row['FIB_50']

        if all([vente_ema, vente_rsi, vente_macd, vente_stoch, vente_sar, vente_fib]):
            data.at[data.index[i], 'Signal'] = 'Vente'

    return data
