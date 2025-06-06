from core.api_fundamentals import get_crypto_fear_greed
from core.learning_tracker import update_learning_from_history
from core.pattern_influence import ajuster_score_par_pattern
import numpy as np

def evaluer_fondamentaux(fundamentals_data):
    if "value" in fundamentals_data:
        return int(fundamentals_data["value"])
    return 50

def evaluer_technique(data):
    rsi = data.get("rsi", 50)
    macd = data.get("macd", 0)
    ema_diff = data.get("ema9", 0) - data.get("ema21", 0)
    boll_band_pos = data.get("bollinger_position", 0.5)
    psar_trend = data.get("psar_trend", "neutral")
    stochastic = data.get("stoch_k", 50)

    score = 50
    if rsi > 65: score += 5
    elif rsi < 35: score -= 5
    if macd > 0: score += 5
    elif macd < 0: score -= 5
    if ema_diff > 0: score += 5
    elif ema_diff < 0: score -= 5
    if boll_band_pos > 0.8: score -= 5
    elif boll_band_pos < 0.2: score += 5
    if psar_trend == "up": score += 5
    elif psar_trend == "down": score -= 5
    if stochastic > 80: score -= 5
    elif stochastic < 20: score += 5
    return max(0, min(100, score))

def evaluer_experience(symbole, source):
    data = update_learning_from_history()
    stats = data.get("strategies", {}).get(source, {})
    taux_reussite = stats.get("taux_reussite", 0.5)
    return int(taux_reussite * 100)

def predire_direction(symbole, data_technique, df_historique, source_strategie):
    score_fondamental = evaluer_fondamentaux(get_crypto_fear_greed())
    score_technique = evaluer_technique(data_technique)
    score_experience = evaluer_experience(symbole, source_strategie)
    bonus_pattern = ajuster_score_par_pattern(df_historique, symbole)

    score_total = (score_fondamental + score_technique + score_experience) / 3 + bonus_pattern
    score_total = max(0, min(100, score_total))

    if score_total >= 60:
        decision = "HAUSSE"
    elif score_total <= 40:
        decision = "BAISSE"
    else:
        decision = "NEUTRE"

    return {
        "prediction": decision,
        "confiance": round(score_total, 2),
        "details": {
            "score_fondamental": score_fondamental,
            "score_technique": score_technique,
            "score_experience": score_experience,
            "bonus_pattern": bonus_pattern
        }
    }