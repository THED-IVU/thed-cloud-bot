import requests
import json
from datetime import datetime

FIREBASE_URL = "https://thed-ivu-bot-default-rtdb.firebaseio.com"

def ajouter_trade_valide(symbole, strategie, score, resultat, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()

    data = {
        "symbole": symbole,
        "strategie": strategie,
        "score": score,
        "resultat": resultat,
        "timestamp": timestamp
    }
    endpoint = f"{FIREBASE_URL}/trades_valides.json"
    try:
        res = requests.post(endpoint, json=data, timeout=5)
        if res.status_code == 200:
            print("✅ Trade IA sauvegardé dans Firebase.")
        else:
            print("⚠️ Erreur de sauvegarde trade:", res.status_code)
    except Exception as e:
        print("❌ Exception Firebase trade:", e)

def ajouter_contexte_detecte(symbole, contexte, timeframe, score, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()

    data = {
        "symbole": symbole,
        "contexte": contexte,
        "timeframe": timeframe,
        "score": score,
        "timestamp": timestamp
    }
    endpoint = f"{FIREBASE_URL}/contextes_ia.json"
    try:
        res = requests.post(endpoint, json=data, timeout=5)
        if res.status_code == 200:
            print("✅ Contexte IA sauvegardé.")
        else:
            print("⚠️ Erreur contexte:", res.status_code)
    except Exception as e:
        print("❌ Exception contexte:", e)

def ajouter_echec_ia(symbole, raison, details, timestamp=None):
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat()

    data = {
        "symbole": symbole,
        "raison": raison,
        "details": details,
        "timestamp": timestamp
    }
    endpoint = f"{FIREBASE_URL}/failures.json"
    try:
        res = requests.post(endpoint, json=data, timeout=5)
        if res.status_code == 200:
            print("⚠️ Échec IA enregistré.")
        else:
            print("❌ Erreur Firebase échec:", res.status_code)
    except Exception as e:
        print("❌ Exception Firebase échec:", e)

def get_trades_historiques(limit=50):
    endpoint = f"{FIREBASE_URL}/trades_valides.json?orderBy=\"timestamp\"&limitToLast={limit}"
    try:
        res = requests.get(endpoint, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return list(data.values()) if data else []
        else:
            print("⚠️ Impossible de récupérer l'historique.")
            return []
    except Exception as e:
        print("❌ Exception Firebase lecture:", e)
        return []