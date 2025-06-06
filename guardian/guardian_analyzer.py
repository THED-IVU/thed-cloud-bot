# guardian/guardian_analyzer.py

import ast

def analyser_fichier(path):
    analyse = {
        "fichier": path,
        "fonctions": [],
        "erreurs": [],
        "imports": [],
        "utilisation": [],
    }

    try:
        with open(path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source, filename=path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                analyse["fonctions"].append(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    analyse["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                analyse["imports"].append(node.module)

    except SyntaxError as e:
        analyse["erreurs"].append(f"Erreur de syntaxe ligne {e.lineno}: {e.msg}")
    except Exception as e:
        analyse["erreurs"].append(str(e))

    return analyse
