# 📄 ping_alert.py

import requests
from datetime import datetime

# Données simulées à envoyer à l'API Flask
payload = {
    "event": "signal_expiration",
    "symbols": ["EURUSD", "GBPUSD"],
    "timestamp": datetime.now().isoformat()
}

# 🔁 Envoi vers l'API (port 5100 par défaut)
url = "http://localhost:5100/alert"

try:
    response = requests.post(url, json=payload)
    print("Statut :", response.status_code)
    print("Réponse :", response.json())
except Exception as e:
    print("❌ Erreur d’envoi :", e)
