# core/strategie_breakout_news.py

import yfinance as yf
from indicators import calculer_tous_les_indicateurs
from datetime import datetime, timedelta

def detecter_opportunite(symbole: str, interval="15m", period="2d", use_ai=False, params=None) -> dict:
    """
    Détecte une cassure de range (breakout asiatique) avec confirmation IA si activée.
    """

    try:
        data = yf.download(symbole, interval=interval, period=period, progress=False).dropna()
        if data.empty or len(data) < 30:
            return None

        data = calculer_tous_les_indicateurs(data, params)
        now = datetime.utcnow()

        # 1. Identifier le range asiatique (23h - 5h UTC de la veille)
        data["hour"] = data.index.hour
        asiatique = data[(data["hour"] >= 23) | (data["hour"] < 5)]
        if asiatique.empty:
            return None

        high_range = asiatique["high"].max()
        low_range = asiatique["low"].min()
        range_median = (high_range + low_range) / 2

        # 2. Dernière bougie
        last = data.iloc[-1]
        close = last["close"]

        breakout_haut = close > high_range * 1.001  # marge de sécurité
        breakout_bas = close < low_range * 0.999

        score = 0
        decision = None
        contexte = []

        # 3. Analyse technique
        if breakout_haut:
            decision = "buy"
            score += 40
            contexte.append("Breakout haut confirmé")
        elif breakout_bas:
            decision = "sell"
            score += 40
            contexte.append("Breakout bas confirmé")
        else:
            return None  # pas de cassure

        # 4. Momentum MACD
        if last["MACD_12_26_9"] > last["MACDs_12_26_9"] and decision == "buy":
            score += 20
            contexte.append("Momentum MACD haussier")
        elif last["MACD_12_26_9"] < last["MACDs_12_26_9"] and decision == "sell":
            score += 20
            contexte.append("Momentum MACD baissier")

        # 5. RSI support
        if decision == "buy" and last["rsi"] > 50:
            score += 10
            contexte.append("RSI > 50")
        elif decision == "sell" and last["rsi"] < 50:
            score += 10
            contexte.append("RSI < 50")

        # 6. IA (optionnelle)
        score_ia = "-"
        validation_ia = "-"
        explication_ia = "-"
        if use_ai:
            from ai import analyser_avec_ia, parser_resultat_ia
            extrait = data.tail(5)[["close", "rsi", "MACD_12_26_9", "MACDs_12_26_9"]].to_string()
            reponse = analyser_avec_ia(extrait)
            infos = parser_resultat_ia(reponse)

            score_ia = infos.get("SCORE", "-")
            validation_ia = infos.get("VALIDATION", "-")
            explication_ia = infos.get("EXPLICATION", "-")

            if validation_ia.lower() == "oui":
                score += 20
                contexte.append("Validé par IA")

        # 7. SL / TP
        entry = round(close, 5)
        sl = round(low_range, 5) if decision == "buy" else round(high_range, 5)
        tp = round(entry * (1.005 if decision == "buy" else 0.995), 5)

        return {
            "decision": decision,
            "score": score,
            "entry": entry,
            "sl": sl,
            "tp": tp,
            "rsi": round(last["rsi"], 2),
            "macd": round(last["MACD_12_26_9"], 5),
            "macds": round(last["MACDs_12_26_9"], 5),
            "ema9": round(last["ema9"], 5),
            "ema21": round(last["ema21"], 5),
            "context": " | ".join(contexte),
            "score_ia": score_ia,
            "validation_ia": validation_ia,
            "explication_ia": explication_ia
        }

    except Exception as e:
        print(f"❌ Erreur dans strategie_breakout_news sur {symbole} : {e}")
        return None
