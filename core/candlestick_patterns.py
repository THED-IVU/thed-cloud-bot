import pandas as pd
import numpy as np
from core.api_fundamentals import get_crypto_fear_greed
from core.learning_tracker import taux_reussite_par_strategie

def detect_patterns(df):
    patterns = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev = df.iloc[i-1]

        open_ = row["Open"]
        close = row["Close"]
        high = row["High"]
        low = row["Low"]

        # Doji : ouverture ≈ fermeture
        if abs(open_ - close) < (high - low) * 0.1:
            patterns.append(("Doji", i))

        # Marubozu (grande bougie sans mèche)
        elif abs(close - open_) > (high - low) * 0.8:
            patterns.append(("Marubozu", i))

        # Marteau : grande mèche basse
        elif (high - max(open_, close)) < (high - low) * 0.3 and (min(open_, close) - low) > (high - low) * 0.6:
            patterns.append(("Hammer", i))

        # Engulfing
        if close > open_ and prev["Close"] < prev["Open"] and close > prev["Open"] and open_ < prev["Close"]:
            patterns.append(("Bullish Engulfing", i))
        elif close < open_ and prev["Close"] > prev["Open"] and close < prev["Open"] and open_ > prev["Close"]:
            patterns.append(("Bearish Engulfing", i))

        # Shooting Star : grande mèche haute
        if (max(open_, close) - low) < (high - low) * 0.3 and (high - max(open_, close)) > (high - low) * 0.6:
            patterns.append(("Shooting Star", i))

    return patterns

def valider_pattern_avec_ia(df, pattern_tuple, strategie="candlestick"):
    pattern_name, index = pattern_tuple
    ligne = df.iloc[index]

    # Analyse fondamentale
    fondamentaux = get_crypto_fear_greed()
    fear_score = int(fondamentaux.get("value", 50))

    # Analyse historique IA
    historique = taux_reussite_par_strategie()
    taux = historique.get(strategie, 50)

    # Logique de validation croisée
    confiance_totale = (taux + fear_score) / 2
    decision = "VALIDÉ" if confiance_totale >= 60 else "REJETÉ"

    return {
        "pattern": pattern_name,
        "timestamp": ligne.name,
        "cours": ligne["Close"],
        "score_ia": taux,
        "score_fonda": fear_score,
        "confiance": round(confiance_totale, 2),
        "decision": decision
    }

# Exemple d’utilisation
if __name__ == "__main__":
    # Exemple DataFrame
    data = {
        "Open": [100, 102, 104, 108, 106, 110],
        "High": [103, 105, 107, 110, 108, 112],
        "Low":  [98, 100, 102, 106, 104, 108],
        "Close": [101, 103, 106, 107, 105, 111]
    }
    df = pd.DataFrame(data)
    df.index = pd.date_range(end=pd.Timestamp.today(), periods=len(df), freq="1D")

    patterns = detect_patterns(df)
    for p in patterns:
        result = valider_pattern_avec_ia(df, p)
        print("🕯️", result)