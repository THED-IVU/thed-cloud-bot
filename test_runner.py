# 📄 test_runner.py – Test rapide sans interface Streamlit
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from ia_alerts import envoyer_alerte_ia
from ia_storage import sauvegarder_analyse, sync_to_firebase

print("🚀 Lancement du test IA global...")

resultat_test = {
    "horodatage": datetime.now().isoformat(),
    "source": "test_console",
    "marche": "EURUSD",
    "horizon": "15min",
    "niveau": "débutant",
    "prediction": "Retournement baissier possible",
    "recommandation": "Vendre à la cassure des 1.0780",
    "score_confiance": 85
}

try:
    print("🔹 Envoi des alertes...")
    envoyer_alerte_ia(resultat_test)

    print("🔹 Sauvegarde locale...")
    sauvegarder_analyse("test_console", resultat_test)

    print("🔹 Synchronisation Firebase...")
    sync_to_firebase("test_console", resultat_test)

    print("✅ Test terminé avec succès.")
except Exception as e:
    print(f"❌ Erreur lors du test : {e}")
