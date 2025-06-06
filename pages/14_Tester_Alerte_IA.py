# pages/14_Tester_Alerte_IA.py

import streamlit as st
from datetime import datetime
import json

# 🔔 Modules pour alerte, logs et Firebase
from notifications.ia_alerts import envoyer_alerte_ia
from ia_storage import sync_to_firebase
from ai_guardian import log_action

# ⚙️ Configuration interface
st.set_page_config(page_title="📢 Test Alerte IA", layout="centered")
st.title("📢 Test Manuel des Alertes IA")

st.info("Ce module permet de tester l'envoi manuel d'une alerte IA stratégique par **Telegram**, **Email**, et de la journaliser dans Firebase + Logs Guardian.")

# 🧠 Exemple d'analyse IA simulée
example_data = {
    "horodatage": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source": "ia_locale",
    "marche": "forex",
    "horizon": "1j",
    "niveau": "professionnel",
    "analyse_technique": "🧮 Croisement EMA + RSI > 60 détecté.",
    "analyse_fondamentale": "📈 L'USD est soutenu par de solides chiffres macro.",
    "contexte_macro": "💬 Taux FED attendu en hausse",
    "risques": "⚠️ Volatilité liée à la guerre commerciale US/Chine",
    "recommandation": "✅ Achat sur USD/JPY à court terme.",
    "prediction": "Probabilité de hausse estimée à 78%",
    "score_confiance": 87
}

# Affichage JSON dans l'interface
st.subheader("🧠 Aperçu du message IA simulé")
st.json(example_data)

# ▶️ Lancement manuel de l'envoi
if st.button("🚀 Envoyer l’alerte IA maintenant"):
    try:
        # 1. 🔔 Envoi alerte IA (Telegram / Email)
        envoyer_alerte_ia(example_data)

        # 2. ☁️ Synchronisation Firebase (si activé dans .env)
        sync_to_firebase("stratégique", example_data)

        # 3. 📝 Journalisation dans Guardian
        log_action("ALERTE_IA_MANUELLE", example_data)

        st.success("✅ Alerte IA envoyée + journalisée avec succès !")

    except Exception as e:
        st.error(f"❌ Échec de l'envoi : {e}")
