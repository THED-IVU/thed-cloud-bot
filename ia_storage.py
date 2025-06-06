# MON_API_PRO/ia_storage.py

import sqlite3
import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

# 🔁 Chargement des variables .env
load_dotenv()

# 🔧 Paramètres extraits depuis .env
DB_PATH = os.getenv("LOCAL_DB_PATH", "MON_API_PRO/ia_analysis.db")
FIREBASE_URL = os.getenv("FIREBASE_DATABASE_URL", "")
FIREBASE_JSON_PATH = os.getenv("FIREBASE_JSON_PATH", "")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
FIREBASE_CLIENT_EMAIL = os.getenv("FIREBASE_CLIENT_EMAIL", "")
FIREBASE_PRIVATE_KEY = os.getenv("FIREBASE_PRIVATE_KEY", "")

# 🔹 Initialisation de la base locale SQLite
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                horodatage TEXT,
                contenu TEXT
            )
        """)
        conn.commit()

# 🔸 1. Sauvegarde dans SQLite
def sauvegarder_analyse(type_analyse: str, contenu: dict):
    """Enregistre une analyse IA dans la base SQLite."""
    init_db()
    horodatage = datetime.now().isoformat()
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO analyses (type, horodatage, contenu)
                VALUES (?, ?, ?)
            """, (type_analyse, horodatage, json.dumps(contenu, ensure_ascii=False)))
            conn.commit()
        print(f"✅ Analyse '{type_analyse}' sauvegardée localement à {horodatage}")
    except Exception as e:
        print(f"❌ Erreur SQLite : {e}")

# 🔸 2. Synchronisation vers Firebase via REST API
def sync_to_firebase(type_analyse: str, contenu: dict):
    """Envoie une analyse vers Firebase si les clés sont valides."""
    if not FIREBASE_URL or not FIREBASE_PROJECT_ID or not FIREBASE_CLIENT_EMAIL or not FIREBASE_PRIVATE_KEY:
        print("⚠️ Clé Firebase absente ou incomplète, synchronisation ignorée.")
        return

    try:
        date_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        url = f"{FIREBASE_URL}/analyses/{type_analyse}/{date_id}.json"

        payload = {
            "timestamp": datetime.now().isoformat(),
            "contenu": contenu
        }

        # Envoi direct sans SDK, via REST (auth publique désactivée si Firebase Rules = true)
        response = requests.put(url, json=payload)
        if response.status_code in [200, 201]:
            print(f"✅ Analyse '{type_analyse}' synchronisée avec Firebase.")
        else:
            print(f"❌ Erreur Firebase : {response.status_code} → {response.text}")
    except Exception as e:
        print(f"❌ Exception Firebase : {e}")
