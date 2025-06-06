# 📁 utils/git_sync.py – GitHub auto-sync avec .env 

import subprocess
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# === Ajout dynamique des chemins ===
current_dir = os.path.dirname(__file__)
root_dir = os.path.abspath(os.path.join(current_dir, ".."))
utils_dir = os.path.join(root_dir, "utils")
if utils_dir not in sys.path:
    sys.path.insert(0, utils_dir)

from utils.path_utils import ajouter_base_et_sous_dossiers
ajouter_base_et_sous_dossiers(["utils"])

# ✅ Charger les variables d’environnement (.env)
dotenv_path = os.path.join(root_dir, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print("⚠️ Fichier .env introuvable, certaines variables peuvent manquer.")

def push_to_github():
    """
    Effectue un commit automatique et un push Git
    en utilisant les informations de configuration issues du fichier .env
    """
    branch = os.getenv("GIT_BRANCH", "main")
    auteur = os.getenv("GIT_COMMIT_AUTHOR", "Bot Auto")
    email = os.getenv("GIT_COMMIT_EMAIL", "bot@example.com")
    repo_name = os.getenv("GIT_REPO_NAME", "repo-inconnu")

    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-sync {timestamp} | {repo_name}"

        subprocess.run(["git", "config", "user.name", auteur], check=True)
        subprocess.run(["git", "config", "user.email", email], check=True)

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", branch], check=True)

        print(f"✅ Commit et push vers GitHub ({branch}) réussi à {timestamp}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git lors du push : {e}")
