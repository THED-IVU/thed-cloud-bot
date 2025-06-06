# core/firebase_sync.py

import firebase_admin
from firebase_admin import credentials, db
import os

# Charger les credentials depuis un fichier JSON sécurisé
FIREBASE_CRED_PATH = os.path.join(os.path.dirname(__file__), "firebase_credentials.json")
FIREBASE_DB_URL = "https://votre-projet.firebaseio.com/"  # Remplacez par votre propre URL

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CRED_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DB_URL
    })

def push_trade_to_firebase(trade_data: dict):
    """Envoie les données d’un trade vers Firebase (sous /trades)."""
    ref = db.reference("/trades")
    ref.push(trade_data)

def get_recent_trades(limit=10):
    """Récupère les X derniers trades."""
    ref = db.reference("/trades")
    data = ref.order_by_key().limit_to_last(limit).get()
    return list(data.values()) if data else []

def push_ia_decision_to_firebase(symbol: str, decision: dict):
    """Ajoute une décision IA dans un sous-chemin spécifique."""
    ref = db.reference(f"/ia_decisions/{symbol}")
    ref.push(decision)
