import requests
import json
import os
from datetime import datetime
from core.rapport_ia import generer_rapport_ia
from fpdf import FPDF

# 🔧 Pour Google Drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# 🔧 Pour Email SMTP
import smtplib
from email.message import EmailMessage

FIREBASE_URL = "https://thed-ivu-bot-default-rtdb.firebaseio.com"
RAPPORTS_PATH = "/rapports_ia"
FULL_ENDPOINT = f"{FIREBASE_URL}{RAPPORTS_PATH}.json"

def sauvegarder_rapport_ia_pdf(periode="semaine"):
    rapport = generer_rapport_ia(periode)
    now = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    filename = f"rapport_ia_{periode}_{now}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, rapport)
    pdf.output(filename)
    print(f"✅ Rapport PDF généré : {filename}")
    return filename

def sauvegarder_rapport_ia_firebase(periode="semaine"):
    rapport = generer_rapport_ia(periode)
    payload = {
        "periode": periode,
        "rapport": rapport,
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        res = requests.post(FULL_ENDPOINT, json=payload, timeout=10)
        if res.status_code == 200:
            print("✅ Rapport IA sauvegardé sur Firebase.")
        else:
            print(f"⚠️ Erreur Firebase : {res.status_code}")
    except Exception as e:
        print("❌ Exception Firebase :", e)

def uploader_pdf_google_drive(filepath):
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()  # Lancer dans navigateur
        drive = GoogleDrive(gauth)

        file_drive = drive.CreateFile({'title': os.path.basename(filepath)})
        file_drive.SetContentFile(filepath)
        file_drive.Upload()
        print("📁 PDF uploadé dans Google Drive")
    except Exception as e:
        print("❌ Erreur Google Drive :", e)

def envoyer_pdf_email(filepath, destinataire):
    try:
        msg = EmailMessage()
        msg["Subject"] = "📊 Rapport IA Hebdomadaire"
        msg["From"] = "tonemail@gmail.com"
        msg["To"] = destinataire
        msg.set_content("Voici le rapport IA de la semaine en pièce jointe.")

        with open(filepath, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=filepath)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("tonemail@gmail.com", "votre_mot_de_passe_app")  # 🛡️ Utilisez un mot de passe d'application
            smtp.send_message(msg)
            print("📧 Email envoyé avec succès.")
    except Exception as e:
        print("❌ Erreur envoi email :", e)