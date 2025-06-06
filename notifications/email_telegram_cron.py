import schedule
import time
from datetime import datetime
from core.report_generator import generer_pdf_journalier
from core.csv_export import exporter_resultats_csv
from notifications.email_alert import envoyer_rapport_email
from notifications.telegram_alert import envoyer_alerte_telegram

def routine_quotidienne():
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        print(f"📆 Lancement de la routine quotidienne à {now}...")

        # 1. Générer le PDF quotidien (analyse IA)
        path_pdf = generer_pdf_journalier()

        # 2. Exporter les données CSV du jour
        path_csv = exporter_resultats_csv()

        # 3. Envoi email avec pièce jointe
        envoyer_rapport_email(path_pdf)

        # 4. Envoi alerte Telegram enrichie
        message = {
            "symbol": "GLOBAL",
            "direction": "Analyse journalière",
            "confiance": 100,
            "mise": "-",
            "duree": "-",
            "contexte": "Synthèse des signaux IA",
            "resume_technique": "📊 Fichier PDF et CSV générés avec succès.",
            "resume_fondamentale": f"📁 Fichiers envoyés à 18h. Vérifiez vos emails ou le dossier partagé."
        }
        envoyer_alerte_telegram(message, "📩 Rapport quotidien IA généré et transmis")

        print("✅ Routine complète exécutée avec succès.")
    except Exception as e:
        print(f"❌ Erreur dans la routine quotidienne : {e}")

# ⏰ Planification automatique chaque jour à 18h
schedule.every().day.at("18:00").do(routine_quotidienne)

if __name__ == "__main__":
    print("🕒 Attente de l’exécution quotidienne à 18h (cron actif)...")
    while True:
        schedule.run_pending()
        time.sleep(60)
