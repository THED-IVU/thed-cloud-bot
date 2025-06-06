import os

def ajouter_init_py_recursif(racine="."):
    fichiers_ajoutes = []
    for dossier, sous_dossiers, fichiers in os.walk(racine):
        if "__pycache__" in dossier:
            continue
        chemin_init = os.path.join(dossier, "__init__.py")
        if not os.path.isfile(chemin_init):
            with open(chemin_init, "w") as f:
                f.write("# Initialisation de package\n")
            fichiers_ajoutes.append(chemin_init)
    return fichiers_ajoutes

# Exemple d’usage
if __name__ == "__main__":
    base = os.path.abspath(".")  # ou spécifie directement ton chemin absolu
    resultats = ajouter_init_py_recursif(base)
    print(f"{len(resultats)} fichiers __init__.py créés :")
    for f in resultats:
        print("✅", f)
