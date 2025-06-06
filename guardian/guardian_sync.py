# guardian/guardian_sync.py

import os
import subprocess
import json
from datetime import datetime

# === CONFIGURATIONS ===
FIREBASE_UPLOAD_PATH = "firebase_sync/"
LOCAL_REPO_PATH = "."
GITHUB_COMMIT_MSG = "🤖 Sync auto via Guardian IA"

# === FONCTION 1 : Affichage arborescence des fichiers ===
def afficher_arborescence(base_path="."):
    arbo = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
        level = root.replace(base_path, "").count(os.sep)
        indent = " " * 2 * level
        arbo.append(f"{indent}📁 {os.path.basename(root)}/")
        for f in files:
            arbo.append(f"{indent}  └── {f}")
    return "\n".join(arbo)

# === FONCTION 2 : Synchronisation GitHub ===
def synchroniser_avec_github():
    try:
        subprocess.run(["git", "add", "."], cwd=LOCAL_REPO_PATH, check=True)
        subprocess.run(["git", "commit", "-m", GITHUB_COMMIT_MSG], cwd=LOCAL_REPO_PATH, check=True)
        subprocess.run(["git", "push"], cwd=LOCAL_REPO_PATH, check=True)
        print(f"[{datetime.now()}] ✅ Synchronisation GitHub réussie.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[{datetime.now()}] ❌ Erreur GitHub (commande) : {e}")
        return False
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erreur GitHub : {e}")
        return False

# === FONCTION 3 : Sauvegarde des logs pour Firebase ===
def synchroniser_avec_firebase(fichier_source="logs/guardian_corrections.log"):
    try:
        if not os.path.exists(fichier_source):
            print(f"[{datetime.now()}] ⚠️ Fichier introuvable : {fichier_source}")
            return False

        os.makedirs(FIREBASE_UPLOAD_PATH, exist_ok=True)
        base_name = os.path.basename(fichier_source)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(FIREBASE_UPLOAD_PATH, f"sync_{timestamp}_{base_name}")
        
        with open(fichier_source, "r", encoding="utf-8") as src:
            contenu = src.read()
        
        with open(dest, "w", encoding="utf-8") as f:
            f.write(contenu)

        print(f"[{datetime.now()}] ✅ Fichier log copié pour Firebase : {dest}")
        return True
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Erreur Firebase Sync : {e}")
        return False

# === MAIN AUTOMATIQUE ===
if __name__ == "__main__":
    print("📦 Arborescence actuelle du projet :")
    print("----------------------------------")
    print(afficher_arborescence("."))

    print("\n🚀 Lancement de la synchronisation Guardian IA...")
    github_result = synchroniser_avec_github()
    firebase_result = synchroniser_avec_firebase()

    if github_result or firebase_result:
        print("✅ Synchronisation globale terminée.")
    else:
        print("⚠️ Aucune synchronisation réussie.")
