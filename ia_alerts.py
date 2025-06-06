# ia_alerts.py – Envoi des alertes IA par Telegram, Email, + sync Firebase

import os
from dotenv import load_dotenv
from datetime import datetime
from notifications.telegram_alert import send_telegram_alert
from notifications.email_cron import envoyer_email_rapport
from ia_storage import sauvegarder_analyse, sync_to_firebase

# 📦 Chargement des clés et paramètres d’environnement
load_dotenv()
ACTIVER_TELEGRAM = os.getenv("ACTIVER_TELEGRAM", "yes").lower() == "yes"
ACTIVER_EMAIL = os.getenv("ACTIVER_EMAIL", "yes").lower() == "yes"
ACTIVER_FIREBASE = os.getenv("ACTIVER_FIREBASE", "yes").lower() == "yes"

def envoyer_alerte_ia(resultat: dict):
    """
    Envoie une alerte formatée par Telegram et/ou Email + sauvegarde locale + sync Firebase.
    - resultat : dict retourné par une analyse IA (locale ou fallback)
    """

    horodatage = resultat.get("horodatage", datetime.now().isoformat())
    source = resultat.get("source", "inconnue")
    marche = resultat.get("marche", "-")
    horizon = resultat.get("horizon", "-")
    niveau = resultat.get("niveau", "-")
    prediction = resultat.get("prediction", "Non précisée")
    recommandation = resultat.get("recommandation", "Non disponible")
    score = resultat.get("score_confiance", "--")

    # ✅ Message formaté pour alertes
    message = f"""
📡 <b>ALERTE IA STRATÉGIQUE</b>
🧠 Source : {source}
🕒 {horodatage}
💱 Marché : {marche} – ⏳ Horizon : {horizon} – 🎓 Niveau : {niveau}
🎯 Recommandation : <b>{recommandation}</b>
📈 Prédiction : {prediction}
🧪 Score de confiance : {score}%
    """.strip()

    # 🔁 Enregistrement local + sync cloud
    try:
        sauvegarder_analyse("alerte_strategique", resultat)
    except Exception as e:
        print(f"⚠️ Erreur lors de la sauvegarde locale : {e}")

    if ACTIVER_FIREBASE:
        try:
            sync_to_firebase("alerte_strategique", resultat)
        except Exception as e:
            print(f"⚠️ Erreur Firebase : {e}")

    # 📲 Telegram
    if ACTIVER_TELEGRAM:
        try:
            send_telegram_alert(message)
            print("✅ Alerte Telegram envoyée.")
        except Exception as e:
            print(f"⚠️ Erreur Telegram : {e}")

    # 📧 Email
    if ACTIVER_EMAIL:
        try:
            sujet = f"🔔 Alerte IA stratégique – {marche.upper()} ({horizon})"
            envoyer_email_rapport(sujet, message.replace("\n", "<br>"))
            print("✅ Alerte Email envoyée.")
        except Exception as e:
            print(f"⚠️ Erreur Email : {e}")
