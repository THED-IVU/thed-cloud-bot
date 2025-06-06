def analyser_resultats(trades):
    resultats = {"gagnés": 0, "perdus": 0}
    for t in trades:
        if t["profit"] > 0:
            resultats["gagnés"] += 1
        else:
            resultats["perdus"] += 1
    return resultats