
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

EMAIL_USER = os.getenv("EMAIL_USER", "bot.thed@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "votre_mot_de_passe")
EMAIL_TO = os.getenv("EMAIL_TO", "destinataire@example.com")

def envoyer_email_rapport(sujet, contenu):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO
        msg['Subject'] = sujet

        msg.attach(MIMEText(contenu, 'html'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        print(f"[{datetime.now()}] ✅ Rapport envoyé par email.")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erreur envoi email : {e}")

def generer_contenu_html_guardian(resultats):
    try:
        html = f"<h2>🛡️ Rapport Guardian IA</h2>"
        html += f"<p>Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        html += f"<p><b>{len(resultats)}</b> fichier(s) corrigé(s) automatiquement :</p><ul>"
        for r in resultats[:10]:
            html += f"<li><b>{r.get('fichier')}</b> – action : {r.get('type')}</li>"
        html += "</ul>"
        if len(resultats) > 10:
            html += f"<p>...et {len(resultats) - 10} autres fichiers.</p>"
        return html
    except Exception as e:
        return f"<p>Erreur dans la génération du contenu : {e}</p>"

if __name__ == "__main__":
    # Test manuel si nécessaire
    dummy = [{"fichier": "core/strategie.py", "type": "replace"}, {"fichier": "core/api.py", "type": "create"}]
    contenu = generer_contenu_html_guardian(dummy)
    envoyer_email_rapport("📊 Rapport Auto – Guardian IA", contenu)
