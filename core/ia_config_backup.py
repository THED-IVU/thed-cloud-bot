import json
import os
from datetime import datetime
import shutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG_PATH = "core/ia_config.json"
BACKUP_FOLDER = "backups/"
EMAIL_RECEIVER = "thedhermann6@gmail.com"

os.makedirs(BACKUP_FOLDER, exist_ok=True)

def send_notification(subject, message):
    sender_email = "yourbotnotifier@gmail.com"  # Remplace si nécessaire
    sender_password = "your_app_password"       # Clé appli Gmail ou SMTP
    receiver_email = EMAIL_RECEIVER

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("📩 Notification email envoyée.")
    except Exception as e:
        print("❌ Échec de l'envoi de notification :", e)

def sauvegarder_config_auto():
    if os.path.exists(CONFIG_PATH):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_FOLDER, f"ia_config_backup_{timestamp}.json")
        shutil.copy(CONFIG_PATH, backup_path)
        msg = f"Sauvegarde effectuée avec succès à {timestamp}."
        print("✅", msg)
        send_notification("✅ Sauvegarde IA réussie", msg)
    else:
        msg = "Fichier de config IA introuvable. Sauvegarde échouée."
        print("⚠️", msg)
        send_notification("❌ Sauvegarde IA échouée", msg)

def exporter_config(nom_fichier="ia_config_export.json"):
    try:
        if os.path.exists(CONFIG_PATH):
            shutil.copy(CONFIG_PATH, nom_fichier)
            msg = f"Fichier exporté : {nom_fichier}"
            print("📤", msg)
            send_notification("✅ Export config IA réussi", msg)
    except Exception as e:
        send_notification("❌ Échec export config IA", str(e))

def importer_config(fichier_import):
    try:
        if os.path.exists(fichier_import):
            shutil.copy(fichier_import, CONFIG_PATH)
            msg = f"Configuration IA importée depuis {fichier_import}"
            print("📥", msg)
            send_notification("✅ Import config IA réussi", msg)
    except Exception as e:
        send_notification("❌ Échec import config IA", str(e))

# Exemple test manuel
if __name__ == "__main__":
    sauvegarder_config_auto()
    # exporter_config()
    # importer_config("ia_config_export.json")