
import json
import requests
import datetime
import os

FIREBASE_URL = os.getenv("FIREBASE_URL")  # Exemple : "https://your-app.firebaseio.com/logs.json"

def log_to_firebase(signal_data):
    if not FIREBASE_URL:
        print("❌ FIREBASE_URL non défini dans les variables d'environnement.")
        return

    payload = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "signal": signal_data
    }

    try:
        response = requests.post(FIREBASE_URL, data=json.dumps(payload))
        if response.status_code == 200:
            print("✅ Signal IA enregistré dans Firebase.")
        else:
            print(f"⚠️ Erreur Firebase : {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception lors de l'envoi Firebase : {e}")
