import schedule
import time
import requests

# 🔧 CONFIGURATION DU BOT TELEGRAM
BOT_TOKEN = "123456789:ABCdefGHI_jklMNOpqrSTUvwxYZ"  # remplace par ton vrai token
CHAT_ID = "123456789"  # ID du groupe ou utilisateur

def send_telegram_report():
    message = "🧠 Rapport IA journalier :\nTous les signaux du jour sont disponibles. Consulte-les dans ton dashboard IA."
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Rapport envoyé sur Telegram.")
        else:
            print(f"❌ Erreur Telegram : {response.text}")
    except Exception as e:
        print(f"❌ Exception Telegram : {e}")

# ⏰ Planification à 18h00
schedule.every().day.at("18:00").do(send_telegram_report)

# 🎯 Boucle infinie
if __name__ == "__main__":
    print("📆 Tâche planifiée : Envoi Telegram tous les jours à 18h.")
    while True:
        schedule.run_pending()
        time.sleep(60)
