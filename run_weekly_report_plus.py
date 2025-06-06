from core.rapport_auto import (
    sauvegarder_rapport_ia_pdf,
    sauvegarder_rapport_ia_firebase,
    uploader_pdf_google_drive,
    envoyer_pdf_email
)

# Étape 1 : Générer le rapport IA en PDF
print("📝 Génération du rapport IA hebdomadaire...")
fichier_pdf = sauvegarder_rapport_ia_pdf("semaine")

# Étape 2 : Sauvegarde dans Firebase
print("☁️ Sauvegarde du rapport dans Firebase...")
sauvegarder_rapport_ia_firebase("semaine")

# Étape 3 : Upload dans Google Drive
print("📤 Envoi du rapport dans Google Drive...")
uploader_pdf_google_drive(fichier_pdf)

# Étape 4 : Envoi par email
print("📧 Envoi du rapport par email...")
destinataire = "destinataire@example.com"  # Remplace par ton adresse Gmail
envoyer_pdf_email(fichier_pdf, destinataire)

print("✅ Rapport IA hebdomadaire généré, synchronisé et partagé.")