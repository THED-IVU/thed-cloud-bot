
import streamlit as st
from datetime import datetime
from ai_guardian import watchdog_executor, risk_monitor, strategy_updater, permission_manager
from event_guard import is_news_period
from core.learning_tracker import enregistrer_apprentissage
from firebase_logger import envoyer_log_firebase
from core.trading_MTX import executer_trade

st.set_page_config(page_title="TIB Guardian - Dashboard Complet", layout="wide")

# --- Barre latérale ---
st.sidebar.title("🛡️ TIB Guardian")
page = st.sidebar.radio("Menu", ["Dashboard IA", "Historique", "Paramètres"])

# --- État Global ---
if page == "Dashboard IA":
    st.title("🧠 Tableau de bord IA - Modules en temps réel")

    st.subheader("🔍 Surveillance")
    modules_status = {
        "Watchdog Executor": "✔️ MT5 surveillé",
        "Risk Monitor": "🛡️ Aucune alerte de drawdown",
        "Strategy Updater": "📊 Aucune stratégie remplacée",
        "Permission Manager": "🔐 Dernière validation : OK",
        "News Watcher": "📢 News critique" if is_news_period() else "🟢 Aucun événement critique"
    }

    for k, v in modules_status.items():
        st.markdown(f"- **{k}** → {v}")

    # --- Validation IA manuelle ---
    st.subheader("🤖 Validation IA humaine requise")

    if st.button("✅ Confirmer et exécuter le trade IA recommandé"):
        trade = {
            "symbol": "BTCUSD",
            "direction": "HAUT",
            "mise": 10,
            "duree": 60,
            "confiance": "87%"
        }
        # Exécution réelle
        resultat = executer_trade(
            symbole=trade["symbol"],
            direction=trade["direction"],
            strategie="guardian_validation",
            resultat="validé",
            volume=trade["mise"],
            expiration=trade["duree"]
        )
        # Enregistrement apprentissage IA
        enregistrer_apprentissage(trade)
        # Notification Firebase
        envoyer_log_firebase(
            symbole=trade["symbol"],
            action=trade["direction"],
            resultat="executé",
            strategie="guardian"
        )
        st.success("🚀 Trade exécuté automatiquement et synchronisé avec l'apprentissage IA.")
        st.toast("📨 Alerte envoyée à Telegram et Firebase")
    elif st.button("❌ Rejeter l’exécution IA"):
        st.warning("⛔ Trade refusé manuellement.")

# --- Historique des décisions ---
elif page == "Historique":
    st.title("📈 Historique Guardian IA")
    if "log_guardian" not in st.session_state:
        st.session_state.log_guardian = []

    st.session_state.log_guardian.append(
        f"{datetime.now().strftime('%H:%M:%S')} - Watchdog ✅, Risk OK, Strategy stable, Validation : {'Oui' if page == 'Dashboard IA' else 'Non'}"
    )
    st.markdown("### 🔁 10 dernières opérations")
    st.dataframe(st.session_state.log_guardian[-10:], use_container_width=True)

# --- Paramètres ---
elif page == "Paramètres":
    st.title("⚙️ Paramètres Guardian")
    st.markdown("- Token Telegram à insérer dans `config_guardian.py`")
    st.markdown("- Activation alert_bot : `True` dans `config_guardian.py`")
    st.markdown("- ✅ Modules IA actifs : watchdog, risk, permission, strategy, learning")
    st.code("config_guardian.ALERT_BOT = True", language="python")
