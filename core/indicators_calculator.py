
import yfinance as yf
import pandas as pd

def calculer_ema(df, period=9):
    return df['Close'].ewm(span=period, adjust=False).mean()

def calculer_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculer_macd(df, short_period=12, long_period=26, signal_period=9):
    ema_short = df['Close'].ewm(span=short_period, adjust=False).mean()
    ema_long = df['Close'].ewm(span=long_period, adjust=False).mean()
    macd = ema_short - ema_long
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal

def calculer_bollinger_bands(df, period=20):
    sma = df['Close'].rolling(window=period).mean()
    std = df['Close'].rolling(window=period).std()
    upper_band = sma + 2 * std
    lower_band = sma - 2 * std
    return upper_band, lower_band

def calculer_stochastic(df, k_period=14, d_period=3):
    low_min = df['Low'].rolling(window=k_period).min()
    high_max = df['High'].rolling(window=k_period).max()
    k = 100 * (df['Close'] - low_min) / (high_max - low_min)
    d = k.rolling(window=d_period).mean()
    return k, d

def recuperer_donnees(symbol, interval='1h', period='7d'):
    data = yf.download(symbol, interval=interval, period=period)
    return data.dropna()

def calculer_tous_les_indicateurs(symbol):
    df = recuperer_donnees(symbol)

    df['EMA_9'] = calculer_ema(df, 9)
    df['EMA_21'] = calculer_ema(df, 21)
    df['RSI'] = calculer_rsi(df, 14)
    df['MACD'], df['MACD_signal'] = calculer_macd(df)
    df['Upper_BB'], df['Lower_BB'] = calculer_bollinger_bands(df)
    df['Stoch_K'], df['Stoch_D'] = calculer_stochastic(df)

    dernier = df.iloc[-1]
    signal_global = 'neutre'
    if dernier['RSI'] < 30 and dernier['MACD'] > dernier['MACD_signal']:
        signal_global = 'achat'
    elif dernier['RSI'] > 70 and dernier['MACD'] < dernier['MACD_signal']:
        signal_global = 'vente'

    signaux = {
        "RSI": round(dernier['RSI'], 2),
        "MACD": round(dernier['MACD'], 4),
        "MACD_signal": round(dernier['MACD_signal'], 4),
        "EMA_9": round(dernier['EMA_9'], 4),
        "EMA_21": round(dernier['EMA_21'], 4),
        "Bollinger_haut": round(dernier['Upper_BB'], 4),
        "Bollinger_bas": round(dernier['Lower_BB'], 4),
        "Stoch_K": round(dernier['Stoch_K'], 2),
        "Stoch_D": round(dernier['Stoch_D'], 2),
        "signal_global": signal_global
    }

    return df, signaux
