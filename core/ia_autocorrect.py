import requests
import json
from collections import Counter
import os

FIREBASE_URL = "https://thed-ivu-bot-default-rtdb.firebaseio.com/failures.json"
PARAM_FILE = "core/ia_config.json"  # Fichier contenant les seuils de stratégie IA

def charger_erreurs(limit=50):
    try:
        res = requests.get(f"{FIREBASE_URL}?orderBy=\"timestamp\"&limitToLast={limit}")
        if res.status_code == 200 and res.json():
            return list(res.json().values())
    except Exception as e:
        print("Erreur chargement Firebase :", e)
    return []

def charger_config():
    if os.path.exists(PARAM_FILE):
        with open(PARAM_FILE, "r") as f:
            return json.load(f)
    return {}

def sauvegarder_config(config):
    with open(PARAM_FILE, "w") as f:
        json.dump(config, f, indent=2)

def correction_auto_post_backtest():
    erreurs = charger_erreurs()
    if not erreurs:
        print("✅ Aucune erreur détectée.")
        return

    config = charger_config()
    seuil_actuel = config.get("seuil_confiance", 60)
    blocages = config.get("strategies_bloc", [])

    symbole_counts = Counter([e["symbole"] for e in erreurs if "symbole" in e])
    raisons = Counter([e["raison"] for e in erreurs if "raison" in e])

    if raisons["confiance trop faible"] >= 5:
        config["seuil_confiance"] = min(100, seuil_actuel + 5)
        print(f"📈 Augmentation du seuil de confiance IA : {seuil_actuel} → {config['seuil_confiance']}")

    if raisons["trop d’échecs"] >= 3:
        suspects = [s for s, c in symbole_counts.items() if c >= 3]
        for s in suspects:
            if s not in blocages:
                blocages.append(s)
        config["strategies_bloc"] = blocages
        print(f"🛑 Blocage temporaire des stratégies pour : {suspects}")

    sauvegarder_config(config)
    print("✅ Ajustements IA enregistrés.")

if __name__ == "__main__":
    correction_auto_post_backtest()