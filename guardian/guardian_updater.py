
# guardian/guardian_updater.py

import time
from datetime import datetime
from guardian_sync import synchroniser_avec_github, synchroniser_avec_firebase
from guardian_organizer import reorganiser_projet

INTERVAL_H = 6  # Toutes les 6 heures
INTERVAL_SECONDES = INTERVAL_H * 3600

def boucle_maj_automatique():
    print(f"[{datetime.now()}] 🧠 Guardian Updater lancé (intervalle = {INTERVAL_H}h)")

    while True:
        print(f"[{datetime.now()}] 🗂 Réorganisation des fichiers...")
        reorganiser_projet()

        print(f"[{datetime.now()}] 🔄 Synchronisation GitHub...")
        synchroniser_avec_github()

        print(f"[{datetime.now()}] ☁️ Préparation pour Firebase...")
        synchroniser_avec_firebase()

        print(f"[{datetime.now()}] ✅ Mise à jour complète. Prochain cycle dans {INTERVAL_H}h.\n")
        time.sleep(INTERVAL_SECONDES)

if __name__ == "__main__":
    boucle_maj_automatique()
