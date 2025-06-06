from core.candlestick_patterns import detect_patterns, valider_pattern_avec_ia

def ajuster_score_par_pattern(df, symbole):
    motifs = detect_patterns(df)
    bonus_total = 0

    for motif in motifs:
        res = valider_pattern_avec_ia(df, motif, strategie="Candlestick")
        if res["decision"] == "VALIDÉ":
            if "Bullish" in res["pattern"] or res["pattern"] == "Hammer":
                bonus_total += 5
            elif "Bearish" in res["pattern"] or res["pattern"] == "Shooting Star":
                bonus_total -= 5

    return bonus_total