
import requests
import json
from datetime import datetime

# 🔐 Ton token de bot Telegram
TELEGRAM_TOKEN = "7523104198:AAHcx-4NMKI00qggdCXOOff0DhLn5TJDTvg"

# 🔁 ID de ton canal ou groupe
TELEGRAM_CHAT_ID = "-1002594620065"

def send_telegram_alert(message: str):
    """Envoi simple d’un message formaté en HTML sur Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"❌ Erreur Telegram : {response.text}")
        else:
            print("✅ Alerte Telegram envoyée.")
    except Exception as e:
        print(f"❌ Exception dans send_telegram_alert : {e}")

def send_ia_trade_summary(data: dict):
    """Envoi enrichi d’un résumé IA complet (stratégie, score, contexte, commentaire IA)."""
    try:
        symbol = data.get("symbole", "Symbole inconnu")
        strategie = data.get("strategie", "Stratégie inconnue")
        direction = data.get("direction", "Direction inconnue")
        score = data.get("score", "Score inconnu")
        contexte = data.get("contexte", "Non précisé")
        decision = data.get("decision", "Non précisée")
        commentaire = data.get("commentaire", "Aucun retour IA")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        message = (
            f"📡 <b>ALERTE IA - {symbol}</b>\n"
            f"🕒 <i>{timestamp}</i>\n"
            f"📊 Stratégie : {strategie}\n"
            f"🔄 Direction : <b>{direction}</b> | 🎯 Score : {score}%\n"
            f"🧠 Contexte : {contexte}\n"
            f"💬 IA : {commentaire}\n"
            f"⚡ <b>Décision IA : {decision}</b>"
        )
        send_telegram_alert(message)
    except Exception as e:
        print(f"❌ Erreur dans send_ia_trade_summary : {e}")

def envoyer_alerte_telegram(trade: dict, titre: str = "🔔 Nouvelle alerte IA"):
    """Format complet incluant résumé technique et fondamental si disponibles."""
    try:
        message = (
            f"{titre}\n\n"
            f"💱 Symbole : {trade.get('symbol', '...')}\n"
            f"📍 Direction : {trade.get('direction', '...')}\n"
            f"🎯 Score de Confiance : {trade.get('confiance', '--')}%\n"
            f"💰 Mise : {trade.get('mise', '--')} $ – 🕒 Durée : {trade.get('duree', '--')} sec\n\n"
            f"🧠 Contexte IA :\n{trade.get('contexte', '...')}\n\n"
            f"📊 Analyse technique :\n{trade.get('resume_technique', '...')}\n\n"
            f"🌐 Analyse fondamentale :\n{trade.get('resume_fondamentale', '...')}"
        )
        send_telegram_alert(message)
    except Exception as e:
        print(f"❌ Erreur dans envoyer_alerte_telegram : {e}")

def envoyer_alerte_guardian(resultats: list):
    """Envoi d'une alerte automatique après corrections du Guardian."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = (
            f"🛡️ <b>Guardian IA - Correctifs Appliqués</b>\n"
            f"🕒 <i>{timestamp}</i>\n"
            f"📂 Fichiers corrigés : {len(resultats)}\n"
        )
        for i, item in enumerate(resultats[:5], 1):  # Afficher jusqu'à 5 fichiers
            message += (
                f"\n🔧 <b>{i}.</b> {item.get('fichier', '...')}\n"
                f"• Action : {item.get('type', '-')}"
            )
        if len(resultats) > 5:
            message += f"\n...et {len(resultats) - 5} autres fichiers corrigés."

        send_telegram_alert(message)
    except Exception as e:
        print(f"❌ Erreur dans envoyer_alerte_guardian : {e}")
