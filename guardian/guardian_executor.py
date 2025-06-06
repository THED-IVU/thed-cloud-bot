# guardian/guardian_executor.py – Correcteur multi-fichier Guardian IA

import os
import json
from datetime import datetime

# === Ajout dynamique des chemins ===
import sys
from utils.path_utils import ajouter_base_et_sous_dossiers
ajouter_base_et_sous_dossiers(["core", "utils", "guardian"])

CORRECTION_LOG_PATH = "logs/guardian_corrections.log"

def executer_correctifs(suggestions):
    """
    Applique les suggestions validées sous forme de :
    - {"type": "create", "fichier": "chemin/vers/fichier.py"}
    - {"type": "replace", "fichier": "chemin/vers/fichier.py"}
    - {"type": "ligne", "fichier": "chemin/vers/fichier.py", "ligne": 42, "correction": "nouvelle_ligne", "fonctionnalite": "xyz"}
    """
    corrections_appliquees = []

    for s in suggestions:
        try:
            fichier = s.get("fichier")
            if not fichier:
                continue

            # Crée les dossiers si besoin
            dossier = os.path.dirname(fichier)
            if dossier and not os.path.exists(dossier):
                os.makedirs(dossier, exist_ok=True)

            if s["type"] == "create":
                with open(fichier, "w", encoding="utf-8") as f:
                    f.write("# Nouveau fichier généré automatiquement par Guardian\n")
                log = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "create",
                    "fichier": fichier
                }
                corrections_appliquees.append(log)

            elif s["type"] == "replace":
                with open(fichier, "w", encoding="utf-8") as f:
                    f.write("# Contenu réécrit automatiquement par Guardian\n")
                log = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "replace",
                    "fichier": fichier
                }
                corrections_appliquees.append(log)

            elif s["type"] == "ligne":
                ligne = s.get("ligne")
                correction = s.get("correction")
                fonctionnalite = s.get("fonctionnalite", "Inconnue")

                if not os.path.isfile(fichier):
                    raise FileNotFoundError(f"Fichier introuvable : {fichier}")

                with open(fichier, "r", encoding="utf-8") as f:
                    contenu = f.readlines()

                if ligne < len(contenu):
                    contenu[ligne] = correction + "\n"
                else:
                    raise IndexError(f"Ligne {ligne} hors des limites de {fichier}")

                with open(fichier, "w", encoding="utf-8") as f:
                    f.writelines(contenu)

                log = {
                    "timestamp": datetime.now().isoformat(),
                    "type": "ligne",
                    "fichier": fichier,
                    "ligne": ligne,
                    "fonctionnalite": fonctionnalite,
                    "correction": correction
                }
                corrections_appliquees.append(log)

            # Log général
            with open(CORRECTION_LOG_PATH, "a", encoding="utf-8") as f_log:
                f_log.write(json.dumps(log) + "\n")

        except Exception as e:
            print(f"❌ Erreur lors de la correction de {s.get('fichier', 'inconnu')} : {e}")

    return corrections_appliquees
