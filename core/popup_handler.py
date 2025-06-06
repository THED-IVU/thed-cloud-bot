
# popup_handler.py – Injection des données IA dans les popups HTML

import os
import json
from jinja2 import Template

TEMPLATE_PATH = "web/popup_modal_ia.html"
OUTPUT_PATH = "web/popup_modal_ia_filled.html"

def generer_popup(resultats_ia):
    """
    Génère un fichier HTML à partir du template en injectant les résultats IA.
    :param resultats_ia: dict contenant direction, score, contexte, technique, fondamental
    """
    if not os.path.exists(TEMPLATE_PATH):
        raise FileNotFoundError(f"Template introuvable : {TEMPLATE_PATH}")

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_html = f.read()

    template = Template(template_html)

    html_rendered = template.render(
        direction=resultats_ia.get("direction", "inconnue"),
        score=resultats_ia.get("score", "-"),
        contexte=resultats_ia.get("contexte", "N/A"),
        technique=resultats_ia.get("res_technique", "Aucune donnée technique"),
        fondamental=resultats_ia.get("res_fondamental", "Aucune donnée fondamentale"),
        decision=resultats_ia.get("decision", "neutre")
    )

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_rendered)

    return OUTPUT_PATH

# Exemple de test local
if __name__ == "__main__":
    exemple = {
        "direction": "achat",
        "score": 82,
        "contexte": "retracement haussier confirmé",
        "res_technique": "EMA9 > EMA21, RSI > 50, MACD croise signal",
        "res_fondamental": "Les marchés anticipent un rebond post-FOMC",
        "decision": "achat"
    }
    chemin = generer_popup(exemple)
    print(f"✅ Popup générée ici : {chemin}")
