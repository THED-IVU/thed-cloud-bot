import requests
import json
import os
from datetime import datetime

# Configuration Firebase (publique mais REST accessible uniquement sur /logs)
FIREBASE_URL = "https://thed-ivu-bot-default-rtdb.firebaseio.com"
FIREBASE_LOG_PATH = "/logs"
FULL_ENDPOINT = f"{FIREBASE_URL}{FIREBASE_LOG_PATH}.json"

# Fichier local de secours si offline ou erreur
FALLBACK_FILE = "fallback_logs.json"

def envoyer_log_firebase(symbole, action, resultat, strategie, score_ia=None, details_ia=None):
    payload = {
        "datetime": datetime.utcnow().isoformat(),
        "symbole": symbole,
        "action": action,
        "resultat": resultat,
        "strategie": strategie,
        "score_ia": score_ia,
        "details_ia": details_ia,
    }

    try:
        response = requests.post(FULL_ENDPOINT, json=payload, timeout=5)
        if response.status_code == 200:
            print("✅ Log Firebase envoyé.")
        else:
            print("⚠️ Échec Firebase. Code:", response.status_code)
            fallback_log(payload)
    except Exception as e:
        print("❌ Erreur envoi Firebase :", e)
        fallback_log(payload)

def fallback_log(payload):
    data = []
    if os.path.exists(FALLBACK_FILE):
        with open(FALLBACK_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    data.append(payload)
    with open(FALLBACK_FILE, "w") as f:
        json.dump(data, f, indent=2)

def synchroniser_fallback():
    if not os.path.exists(FALLBACK_FILE):
        print("Aucun fichier fallback à synchroniser.")
        return

    with open(FALLBACK_FILE, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Fichier fallback corrompu.")
            return

    success = 0
    for log in logs:
        try:
            res = requests.post(FULL_ENDPOINT, json=log, timeout=5)
            if res.status_code == 200:
                success += 1
        except:
            continue

    if success > 0:
        print(f"✅ {success} log(s) resynchronisés avec Firebase.")
        os.remove(FALLBACK_FILE)
    else:
        print("❌ Aucun log n’a pu être resynchronisé.")