
import json
import os

def enregistrer_feedback(trade_info, resultat="succès"):
    dossier = "learning_logs"
    os.makedirs(dossier, exist_ok=True)
    fichier = os.path.join(dossier, "feedbacks.json")
    try:
        contenu = json.load(open(fichier)) if os.path.exists(fichier) else []
    except:
        contenu = []

    feedback = {
        "datetime": trade_info["datetime"],
        "symbol": trade_info["symbol"],
        "direction": trade_info["direction"],
        "confiance": trade_info["confiance"],
        "résultat": resultat
    }

    contenu.append(feedback)
    with open(fichier, "w") as f_out:
        json.dump(contenu, f_out, indent=2)
