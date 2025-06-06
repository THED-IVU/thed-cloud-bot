
import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="TIB Guardian - Notifications IA", layout="wide")
st.title("🛡️ Notifications IA en temps réel (TIB Guardian)")

# Simulations des résultats du Guardian IA (à remplacer par des appels réels)
modules = {
    "watchdog_executor": "MT5 fonctionnel ✅",
    "risk_monitor": "Risque sous contrôle ✔️ (Drawdown 2.5%)",
    "strategy_updater": "Switch stratégique suggéré : EMA vers Heikin-Ashi",
    "permission_manager": "✅ Permission validée automatiquement",
    "learning_sync": "Apprentissage IA synchronisé à 10:40",
    "multi_env_tracker": "Signaux alignés : MT5 + KuCoin 📊",
    "alert_bot": "⚠️ Alerte désactivée (activer dans config_guardian.py)",
    "web_news_watcher": "📢 News impactante détectée : FOMC dans 30min",
    "ai_opportunity_scanner": "Nouvelle IA détectée : finetuned-RSI-v3 🤖",
    "platform_connector": "💻 Plateforme KuCoin détectée & prête",
    "ux_optimizer": "💡 Suggestion UI : Ajouter slider de délai sur PocketOption"
}

# Simule un message IA popup toutes les 15s max
module = random.choice(list(modules.items()))
st.info(f"🧠 [{module[0]}] → {module[1]} ({datetime.now().strftime('%H:%M:%S')})")

# Historique des dernières notifications (à rendre persistant avec DB si besoin)
if "historique" not in st.session_state:
    st.session_state.historique = []

st.session_state.historique.append(f"{datetime.now().strftime('%H:%M:%S')} — {module[0]}: {module[1]}")
st.markdown("### 🕒 Historique des alertes IA")
st.write(st.session_state.historique[-10:])  # Affiche les 10 dernières
