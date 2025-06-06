import time
import schedule
from core.ia_config_backup import sauvegarder_config_auto

def job():
    print("📂 Sauvegarde hebdomadaire de la config IA...")
    sauvegarder_config_auto()

schedule.every().sunday.at("21:00").do(job)
print("⏰ Sauvegarde planifiée chaque dimanche à 21:00.")

while True:
    schedule.run_pending()
    time.sleep(60)