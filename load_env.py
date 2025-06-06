# 🔁 load_env.py – Chargement automatique des variables d’environnement
import os
from dotenv import load_dotenv

def charger_variables_env(fichier_env=".env"):
    """
    Charge les variables d’environnement depuis un fichier .env spécifié.
    Par défaut, il charge le fichier .env à la racine du projet.
    """
    try:
        chemin_absolu = os.path.abspath(fichier_env)
        if os.path.exists(chemin_absolu):
            load_dotenv(chemin_absolu)
            print(f"✅ Variables d’environnement chargées depuis : {chemin_absolu}")
        else:
            print(f"❌ Fichier .env introuvable à : {chemin_absolu}")
    except Exception as e:
        print(f"⚠️ Erreur lors du chargement du fichier .env : {e}")
