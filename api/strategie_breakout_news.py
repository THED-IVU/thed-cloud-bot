# 📄 Fichier : core/strategie_breakout_news.py

import yfinance as yf
import pandas as pd
from indicators import calculer_tous_les_indicateurs
from ai import analyser_avec_ia, parser_resultat_ia

# Paramètres
PLAGE_HORAIRE = ("23:00", "05:00")  # Range asiatique
SEUIL_ATR = 0.0008  # Seuil minimal de volatilité pour un breakout


def detecter_opportunite(symbol: str, interval="15m", period="2d") -> dict:
    try:
        data = yf.download(symbol, interval=interval, period=period, progress=False).dropna()
        data = calculer_tous_les_indicateurs(data)

        # 1. Détecter le range asiatique (de 23h à 5h UTC)
        data["heure"] = data.index.strftime("%H:%M")
        range_data = data[data["heure"].between(*PLAGE_HORAIRE)]
        if range_data.empty:
            return {"decision": "HOLD", "score": 50, "sl": 15, "tp": 25, "comment": "Aucune donnée pour le range asiatique"}

        high_range = range_data["high"].max()
        low_range = range_data["low"].min()
        range_size = high_range - low_range

        # 2. Détecter cassure du range actuel
        dernier = data.iloc[-1]
        prix = dernier["close"]
        atr = dernier.get("volatilite", range_size / prix)

        cassure_haut = prix > high_range and atr > SEUIL_ATR
        cassure_bas = prix < low_range and atr > SEUIL_ATR

        # 3. Analyse IA pour valider le sens fondamental (si dispo)
        prompt = data.tail(5).to_string()
        reponse_ia = analyser_avec_ia(prompt)
        analyse = parser_resultat_ia(reponse_ia)
        tendance_ia = analyse.get("TREND", "N/A")
        score_ia = int(analyse.get("SCORE", "0/10").split("/")[0]) * 10

        # 4. Combiner
        if cassure_haut and "bull" in tendance_ia.lower():
            return {"decision": "BUY", "score": score_ia, "sl": int(range_size * 10000), "tp": int(range_size * 20000), "comment": "Cassure haussière + IA haussière"}
        elif cassure_bas and "bear" in tendance_ia.lower():
            return {"decision": "SELL", "score": score_ia, "sl": int(range_size * 10000), "tp": int(range_size * 20000), "comment": "Cassure baissière + IA baissière"}
        else:
            return {"decision": "HOLD", "score": 60, "sl": 15, "tp": 30, "comment": "Aucune cassure valide confirmée"}

    except Exception as e:
        return {"decision": "HOLD", "score": 0, "sl": 15, "tp": 30, "comment": f"Erreur: {e}"}
