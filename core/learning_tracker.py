import json
import os
from datetime import datetime
from collections import defaultdict
import csv

DB_PATH = "learning_data/historique_ia.json"
CSV_PATH = "learning_data/historique_ia.csv"
os.makedirs("learning_data", exist_ok=True)

def enregistrer_resultat(trade):
    try:
        if os.path.exists(DB_PATH):
            with open(DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except:
        data = []

    trade["timestamp"] = datetime.now().isoformat()
    data.append(trade)

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    _sauvegarder_csv(data)

def charger_historique():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def sauvegarder_historique(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    _sauvegarder_csv(data)

def _sauvegarder_csv(data):
    if not data:
        return
    with open(CSV_PATH, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = sorted(list(set().union(*(d.keys() for d in data))))
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def ajouter_resultat(symbole, strategie, resultat, user_feedback=None):
    historique = charger_historique()
    historique.append({
        "symbole": symbole,
        "strategie": strategie,
        "resultat": resultat,
        "feedback": user_feedback,
        "timestamp": datetime.now().isoformat()
    })
    sauvegarder_historique(historique)

def taux_reussite_par_strategie():
    historique = charger_historique()
    stats = defaultdict(lambda: {"gagne": 0, "perdu": 0})

    for h in historique:
        s = h.get("strategie", "inconnue")
        if h.get("resultat") == "gagné":
            stats[s]["gagne"] += 1
        elif h.get("resultat") == "perdu":
            stats[s]["perdu"] += 1

    taux = {}
    for s, r in stats.items():
        total = r["gagne"] + r["perdu"]
        taux[s] = round((r["gagne"] / total) * 100, 2) if total > 0 else 0.0
    return taux

if __name__ == "__main__":
    ajouter_resultat("BTC-USD", "EMA+RSI", "gagné", "Bon timing, mais un peu court")
    ajouter_resultat("EURUSD=X", "Breakout", "perdu", "Signal trop tardif")
    print("📊 Taux de réussite par stratégie :")
    print(taux_reussite_par_strategie())
