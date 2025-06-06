# guardian/guardian_suggestions.py

def generer_suggestions(rapport):
    suggestions = []
    for r in rapport:
        if r["status"] == "absent":
            suggestions.append({
                "titre": f"Créer {r['fichier']}",
                "description": "Le fichier est manquant. Création d’un squelette fonctionnel proposé.",
                "avantage": "Rétablit la structure manquante",
                "inconvenient": "Code de base générique",
                "type": "create",
                "fichier": r["fichier"],
                "impact": 90  # Impact fort car fichier critique manquant
            })
        elif r["status"] == "vide ou incomplet":
            suggestions.append({
                "titre": f"Corriger {r['fichier']}",
                "description": "Le fichier semble incomplet. Propose de réécrire un modèle fonctionnel.",
                "avantage": "Remise en conformité rapide",
                "inconvenient": "Écrase le contenu actuel",
                "type": "replace",
                "fichier": r["fichier"],
                "impact": 70  # Impact moyen à fort
            })
        elif r["status"].startswith("erreur"):
            suggestions.append({
                "titre": f"Analyser {r['fichier']}",
                "description": f"Erreur d’accès ou de lecture : {r['status']}",
                "avantage": "Détection précoce d’instabilité",
                "inconvenient": "Peut nécessiter une inspection manuelle",
                "type": "replace",
                "fichier": r["fichier"],
                "impact": 80  # Prioritaire
            })
    return suggestions
