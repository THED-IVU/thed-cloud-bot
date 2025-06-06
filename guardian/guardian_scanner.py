# guardian/guardian_scanner.py – Scanner de conformité Guardian IA

import os
import json
from datetime import datetime
import sys

# === Ajout dynamique des chemins ===
from utils.path_utils import ajouter_base_et_sous_dossiers
ajouter_base_et_sous_dossiers(["utils", "core", "guardian"])

# 🔒 Dossiers à ignorer
DOSSIERS_EXCLUS = ["__pycache__", ".venv", ".git", "venv", "env"]

# 📁 Dossier et fichier de logs
LOG_DIR = "guardian_logs"
LOG_PATH = os.path.join(LOG_DIR, "scanner_report.log")
JSON_EXPORT = os.path.join(LOG_DIR, "dernier_scan.json")
os.makedirs(LOG_DIR, exist_ok=True)

def smart_diagnostics():
    print("🧠 Analyse IA lancée pour les anomalies détectées... (placeholder)")
    # TODO : Intégrer une vraie analyse GPT ou locale

def scanner_complet(racine=".", extensions=[".py"], export_json=True):
    rapport = []
    anomalies = False

    for root, dirs, files in os.walk(racine):
        # 🔒 Filtrer les dossiers exclus
        dirs[:] = [d for d in dirs if d not in DOSSIERS_EXCLUS]

        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                chemin = os.path.join(root, file)
                try:
                    with open(chemin, "r", encoding="utf-8") as f:
                        contenu = f.read()
                        status = "ok"

                        if "def " not in contenu and "class " not in contenu:
                            status = "vide"
                        elif "TODO" in contenu or "FIXME" in contenu:
                            status = "à corriger"
                            anomalies = True
                except Exception as e:
                    status = f"erreur: {e}"
                    anomalies = True

                rapport.append({
                    "fichier": chemin.replace("\\", "/"),
                    "status": status
                })

    # 📤 Export JSON
    if export_json:
        with open(JSON_EXPORT, "w", encoding="utf-8") as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)

    # 📝 Log texte
    with open(LOG_PATH, "a", encoding="utf-8") as logf:
        logf.write(f"\n[{datetime.now().isoformat()}] 🔍 Scan exécuté – {len(rapport)} fichiers\n")
        for ligne in rapport:
            logf.write(f"{ligne['fichier']} => {ligne['status']}\n")

    # 🧠 Diagnostic IA si besoin
    if anomalies:
        smart_diagnostics()

    return rapport
