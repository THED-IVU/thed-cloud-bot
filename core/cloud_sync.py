import requests
import json
from db import lire_trades
from datetime import datetime

FIREBASE_URL = "https://thed-ivu-bot-default-rtdb.firebaseio.com"
FIREBASE_LOG_PATH = "/logs"
FULL_ENDPOINT = f"{FIREBASE_URL}{FIREBASE_LOG_PATH}.json"

def envoyer_vers_firebase(data):
    try:
        res = requests.post(FULL_ENDPOINT, json=data, timeout=5)
        return res.status_code == 200
    except:
        return False

def synchroniser_historique_firebase():
    trades = lire_trades()
    if trades.empty:
        print("Aucun trade à synchroniser.")
        return

    success, total = 0, 0
    for _, row in trades.iterrows():
        total += 1
        payload = {
            "datetime": row.get("datetime", datetime.utcnow().isoformat()),
            "symbole": row.get("asset", "?"),
            "action": row.get("action", "?"),
            "resultat": "gagné" if row.get("profit", 0) > 0 else "perdu",
            "strategie": row.get("source", "inconnue"),
            "score_ia": row.get("score_ia", None),
            "details_ia": {
                "score_fondamental": None,
                "score_technique": row.get("note", None),
                "score_experience": None
            }
        }
        if envoyer_vers_firebase(payload):
            success += 1

    print(f"✅ {success}/{total} trade(s) synchronisés avec Firebase.")