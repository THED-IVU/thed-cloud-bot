import time
import schedule
from core.rapport_auto import (
    sauvegarder_rapport_ia_pdf,
    sauvegarder_rapport_ia_firebase,
    uploader_pdf_google_drive,
    envoyer_pdf_email
)

def executer_rapport_ia():
    print("📊 Génération automatique du rapport IA hebdomadaire...")

    # Étape 1 : Générer le PDF
    fichier_pdf = sauvegarder_rapport_ia_pdf("semaine")

    # Étape 2 : Sauvegarde dans Firebase
    sauvegarder_rapport_ia_firebase("semaine")

    # Étape 3 : Upload Google Drive
    uploader_pdf_google_drive(fichier_pdf)

    # Étape 4 : Envoi Email
    destinataire = "thedhermann6@gmail.com"
    envoyer_pdf_email(fichier_pdf, destinataire)

    print("✅ Rapport IA hebdomadaire généré, sauvegardé et partagé.\n")

# Paramètres utilisateur
MODE = "manuel"  # "manuel" ou "auto"
JOUR_HEURE = "sunday 20:00"  # Format 'jour heure'

if MODE == "manuel":
    print("🧠 Mode manuel activé. Lancement immédiat...")
    executer_rapport_ia()

elif MODE == "auto":
    jour, heure = JOUR_HEURE.split()
    schedule.every().__getattribute__(jour).at(heure).do(executer_rapport_ia)
    print(f"⏰ Mode auto activé. Rapport sera généré chaque {JOUR_HEURE}.")

    while True:
        schedule.run_pending()
        time.sleep(30)