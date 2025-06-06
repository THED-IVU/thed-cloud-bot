from core.candlestick_patterns import detect_patterns, valider_pattern_avec_ia

def strategie_candles(df, symbole):
    resultats = []
    motifs = detect_patterns(df)

    for p in motifs:
        analyse = valider_pattern_avec_ia(df, p, strategie="Candlestick")
        if analyse["decision"] == "VALIDÉ":
            resultats.append({
                "symbole": symbole,
                "signal": "BUY" if "Bullish" in analyse["pattern"] or analyse["pattern"] == "Hammer" else "SELL",
                "pattern": analyse["pattern"],
                "score": analyse["confiance"]
            })

    return resultats