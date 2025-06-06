# test_runner_prod.py – Test réel de l'API IA et intégration complète

import requests
import json
from datetime import datetime
from ia_alerts import envoyer_alerte_ia
from ia_storage import sauvegarder_analyse, sync_to_firebase

API_URL = "http://localhost:8000/analyse_strategique"

params = {
    "marche": "forex",
    "horizon": "1j",
    "niveau": "professionnel"
}

print("🔄 Lancement de l’analyse stratégique réelle depuis l’API...")
try:
    response = requests.get(API_URL, params=params)
    data = response.json()
    resultat = data.get("resultat", {})

    if not resultat:
        print("❌ Aucune donnée retournée par l’API.")
    else:
        print("✅ Résultat API obtenu :")
        print(json.dumps(resultat, indent=2, ensure_ascii=False))

        # Ajout de quelques métadonnées si absentes
        resultat["source"] = data.get("source", "API")
        resultat["horodatage"] = resultat.get("horodatage", datetime.now().isoformat())

        # 🔔 Alerte IA (Email/Telegram)
        print("📡 Envoi des alertes IA...")
        envoyer_alerte_ia(resultat)

        # 💾 Sauvegarde locale et Firebase
        print("📦 Sauvegarde dans SQLite...")
        sauvegarder_analyse("test_prod", resultat)

        print("☁️ Synchronisation Firebase...")
        sync_to_firebase("test_prod", resultat)

        print("📝 Test global IA terminé avec succès.")

except Exception as e:
    print(f"❌ Erreur pendant le test global : {e}")
