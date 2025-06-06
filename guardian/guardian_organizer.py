
# guardian/guardian_organizer.py

import os
import shutil
from pathlib import Path

# Structure cible par défaut
STRUCTURE_CIBLE = {
    "core": ["executor", "manager", "strategy", "trading", "learning", "data"],
    "pages": ["dashboard", "bot", "config", "admin", "planificateur"],
    "guardian": ["scanner", "executor", "suggestions", "reporter", "scheduler", "organizer", "updater"],
    "logs": [],
    "modules": [],
    "tests": [],
}

EXCLUSIONS = [".git", "__pycache__", "venv", "node_modules", "env"]

def identifier_repertoire_cible(nom_fichier):
    """Heuristique simple pour classer le fichier dans un dossier logique."""
    nom = nom_fichier.lower()
    for dossier, mots_cles in STRUCTURE_CIBLE.items():
        if any(m in nom for m in mots_cles):
            return dossier
    return "modules"  # par défaut si non classable

def reorganiser_projet(racine="."):
    deplacements = []
    for root, dirs, files in os.walk(racine):
        dirs[:] = [d for d in dirs if d not in EXCLUSIONS]
        for file in files:
            if file.endswith(".py") and "guardian_organizer.py" not in file:
                chemin_actuel = Path(root) / file
                destination_dir = identifier_repertoire_cible(file)
                chemin_cible = Path(racine) / destination_dir / file

                if not chemin_cible.exists():
                    Path(racine, destination_dir).mkdir(parents=True, exist_ok=True)
                    shutil.move(str(chemin_actuel), str(chemin_cible))
                    deplacements.append({
                        "fichier": file,
                        "depuis": str(chemin_actuel),
                        "vers": str(chemin_cible)
                    })

    return deplacements

if __name__ == "__main__":
    resultat = reorganiser_projet(".")
    print("✅ Réorganisation terminée.")
    for r in resultat:
        print(f"📁 {r['fichier']} déplacé vers {r['vers']}")
