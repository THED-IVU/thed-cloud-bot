# ✅ utils/path_utils.py

import os
import sys

def ajouter_dossier_au_sys_path(*dossiers_relatifs):
    """
    Ajoute un ou plusieurs dossiers au sys.path de manière sécurisée.

    Paramètres :
    - *dossiers_relatifs : Un ou plusieurs chemins relatifs à partir du fichier appelant.

    Exemple :
        ajouter_dossier_au_sys_path("..", "notifications")
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))
    for chemin in dossiers_relatifs:
        chemin_absolu = os.path.abspath(os.path.join(base_dir, chemin))
        if chemin_absolu not in sys.path:
            sys.path.append(chemin_absolu)

def ajouter_base_et_sous_dossiers(sous_dossiers=None):
    """
    Ajoute automatiquement les principaux sous-dossiers utiles du projet au sys.path.

    Si aucun argument n’est fourni, ajoute par défaut :
    - Racine du projet
    - /core
    - /guardian
    - /notifications
    - /utils
    - /MON_API_PRO
    - /ia

    Paramètres :
    - sous_dossiers : liste personnalisée des dossiers à inclure. Sinon, la liste par défaut est utilisée.
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    if sous_dossiers is None:
        sous_dossiers = ["core", "guardian", "notifications", "utils", "MON_API_PRO", "ia"]

    chemins = [base_dir] + [os.path.join(base_dir, d) for d in sous_dossiers]

    for chemin in chemins:
        if chemin not in sys.path:
            sys.path.append(chemin)
