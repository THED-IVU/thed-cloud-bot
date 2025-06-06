# 📄 pages/14_Tests_Fonctions_IA.py – Test complet IA, alertes, Firebase, SQLite

import streamlit as st
from datetime import datetime
from ia_alerts import envoyer_alerte_ia
from ia_storage import sauvegarder_analyse, sync_to_firebase

st.set_page_config(page_title="✅ Test IA & Alertes", layout="centered")
st.title("🧪 Test global des fonctions IA & alertes")

st.info("Ce bouton va simuler une alerte stratégique IA complète, avec enregistrement local, alertes Telegram/Email, et synchronisation Firebase.")

if st.button("🚀 Lancer le test global maintenant"):

    # 🔁 Exemple de résultat IA simulé
    resultat_test = {
        "horodatage": datetime.now().isoformat(),
        "source": "test_ia_locale",
        "marche": "BTCUSD",
        "horizon": "1h",
        "niveau": "expert",
        "prediction": "Hausse probable après consolidation",
        "recommandation": "Acheter si breakout confirmé au-dessus de 68 000 $",
        "score_confiance": 92
    }

    # ✅ Test de chaque fonction
    try:
        st.write("🔹 Envoi des alertes...")
        envoyer_alerte_ia(resultat_test)

        st.write("🔹 Sauvegarde locale (SQLite)...")
        sauvegarder_analyse("test_alertes", resultat_test)

        st.write("🔹 Synchronisation Firebase...")
        sync_to_firebase("test_alertes", resultat_test)

        st.success("🎉 Test complet effectué avec succès.")
    except Exception as e:
        st.error(f"❌ Erreur lors du test : {e}")
