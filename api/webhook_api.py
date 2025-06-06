# 📄 Fichier : api/webhook_api.py

from flask import Flask, request, jsonify
from datetime import datetime
import logging
import os
import requests

app = Flask(__name__)

# ✉️ CONFIG NOTIFICATIONS (Discord / Telegram)
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK", "")  # Ex: https://discord.com/api/webhooks/... 
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Dossier logs d'alertes
os.makedirs("logs", exist_ok=True)
log_file = os.path.join("logs", "webhook_alerts.log")
logging.basicConfig(filename=log_file, level=logging.INFO)


def notifier_discord(message):
    if DISCORD_WEBHOOK_URL:
        try:
            requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        except Exception as e:
            logging.warning(f"Erreur Discord: {e}")


def notifier_telegram(message):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
            requests.post(url, data=data)
        except Exception as e:
            logging.warning(f"Erreur Telegram: {e}")


@app.route("/alert", methods=["POST"])
def recevoir_alerte():
    data = request.json

    if not data:
        return jsonify({"status": "error", "message": "Données JSON requises"}), 400

    event = data.get("event")
    symbols = data.get("symbols", [])
    timestamp = data.get("timestamp", datetime.now().isoformat())

    # Message formaté
    msg = f"\ud83d\udea8 [ALERTE BOT] \n\n✨ Type: {event}\n⚖️ Symboles: {', '.join(symbols)}\n⏰ Heure: {timestamp}"

    # Log interne
    logging.info(msg)
    print(msg)

    # Notifs externes
    notifier_discord(msg)
    notifier_telegram(msg)

    return jsonify({
        "status": "received",
        "received": {
            "event": event,
            "symbols": symbols,
            "timestamp": timestamp
        }
    })

if __name__ == "__main__":
    app.run(debug=True, port=5100)
