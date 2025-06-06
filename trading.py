from streamlit_autorefresh import st_autorefresh

import streamlit as st
import pandas as pd
import os
from datetime import datetime
import logging
import matplotlib.pyplot as plt
import base64
import requests

from config_state import sidebar_config
from runtime_config import get_runtime_config
from indicators import calculer_tous_les_indicateurs
from ai import analyser_avec_ia
from trading import enregistrer_trade, lire_trades

from core.core_bot import run_bot
from core.risk_manager import TradeManager
from core.trading_MTX import cloturer_ordre

st.set_page_config(page_title="Live Bot", layout="wide")
sidebar_config()
CONFIG = get_runtime_config()
use_ai = CONFIG.get("use_ai", False)

if "bot_actif" not in st.session_state:
    st.session_state.bot_actif = False
if "trade_manager" not in st.session_state:
    st.session_state.trade_manager = TradeManager(capital=1000)

st.sidebar.header("⚙️ Paramètres Bot IA")
symbol = st.sidebar.text_input("📈 Actif graphique", value="EURUSD=X")
interval = st.sidebar.selectbox("⏱ Intervalle graphique", ["1m", "5m", "15m", "1h"], index=0)
freq_minutes = st.sidebar.slider("🔁 Fréquence d'exécution (min)", 1, 60, value=1)
max_trades = st.sidebar.slider("🔒 Max trades par jour", 1, 20, value=10)
webhook_url = st.sidebar.text_input("🌐 Webhook d'alerte (optionnel)", value="")
st.session_state.trade_manager.max_trades_per_day = max_trades

if st.session_state.bot_actif:
    st_autorefresh(interval=freq_minutes * 60 * 1000, key="refresh_bot")

st.title("📱 Suivi en temps réel du Bot de Trading IA")
col1, col2 = st.columns([2, 1])
with col1:
    bouton = st.button("▶️ Activer le bot" if not st.session_state.bot_actif else "⏹ Désactiver le bot")
    if bouton:
        st.session_state.bot_actif = not st.session_state.bot_actif
        st.success("✅ Bot activé" if st.session_state.bot_actif else "🔚 Bot désactivé")
with col2:
    statut = "🟢 Actif" if st.session_state.bot_actif else "🔴 Inactif"
    st.metric("Statut", statut)

log_placeholder = st.empty()
chart_placeholder = st.empty()
trade_table = st.empty()
alert_log = st.container()
expired_container = st.expander("🔒 Signaux expirés récemment", expanded=False)
col_stats_1, col_stats_2 = st.columns(2)

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"live_bot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(filename=log_file, level=logging.INFO)

if st.session_state.bot_actif:
    st.session_state.trade_manager.check_auto_reset()

    if st.session_state.trade_manager.trades_today >= st.session_state.trade_manager.max_trades_per_day:
        st.warning("🔒 Limite de trades journaliers atteinte. Le bot est en pause.")
    else:
        with st.spinner("📈 Analyse en cours..."):
            run_bot()
        st.success(f"✅ Analyse terminée à {datetime.now().strftime('%H:%M:%S')}")
        log_placeholder.success("✅ Exécution complète.")

    try:
        df = lire_trades()
        if not df.empty:
            now = datetime.now()
            df["datetime"] = pd.to_datetime(df["datetime"])

            def calculer_chrono(row):
                priorites = {
                    "Sniper IA": 30,
                    "Breakout + News": 25,
                    "Heikin Ashi + PSAR": 20,
                    "Fibonacci + Bougies": 15,
                    "EMA + RSI + MACD": 10
                }
                max_secs = priorites.get(row["source"], 15)
                elapsed = (now - row["datetime"]).total_seconds()
                remaining = max(0, int(max_secs - elapsed))
                return f"{remaining}s", remaining

            df[["⏳ Viabilité", "temps_restant"]] = df.apply(lambda row: pd.Series(calculer_chrono(row)), axis=1)
            df_valides = df[df["temps_restant"] > 0].copy()
            df_expired = df[df["temps_restant"] == 0].copy()

            if not df_expired.empty:
                with expired_container:
                    st.dataframe(df_expired.drop(columns=["temps_restant"]), use_container_width=True)

            if df_valides["temps_restant"].min() <= 5:
                st.warning("⚠️ Certains signaux expirent dans moins de 5 secondes !")
                symbols_expired = df[df["temps_restant"] <= 0]["asset"].unique()
                for sym in symbols_expired:
                    cloturer_ordre(sym)
                    st.info(f"🔒 Position expirée sur {sym} automatiquement cloturée.")

                if webhook_url:
                    payload = {
                        "event": "signal_expiration",
                        "symbols": list(symbols_expired),
                        "timestamp": datetime.now().isoformat()
                    }
                    try:
                        requests.post(webhook_url, json=payload)
                    except Exception as err:
                        st.error(f"Webhook non envoyé : {err}")

                with alert_log:
                    st.error(f"🚨 Alertes critiques : {', '.join(symbols_expired)}")

            with st.expander("🤮 Détails IA / Techniques complets"):
                filtre = st.selectbox("🌟 Filtrer les signaux IA par:", ["Tous", "Score IA >= 7", "Validation IA = Oui"])
                df_filtré = df_valides.copy()
                if filtre == "Score IA >= 7":
                    df_filtré = df_filtré[df_filtré["score_ia"].apply(lambda x: float(x) if x != '-' else 0) >= 7]
                elif filtre == "Validation IA = Oui":
                    df_filtré = df_filtré[df_filtré["validation_ia"].str.lower() == "oui"]

                for i, row in df_filtré.tail(10).iterrows():
                    with st.expander(f"{row['datetime']} | {row['asset']} | {row['action']}"):
                        st.markdown(f"**Score IA**: {row['score_ia']}")
                        st.markdown(f"**Validation IA**: {row['validation_ia']}")
                        st.markdown(f"**Explication IA**: {row['explication_ia']}")

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📃 Export CSV en direct", csv, file_name="live_signaux_complets.csv", mime="text/csv")

    except Exception as e:
        logging.error(str(e))
        st.error(f"Erreur affichage : {e}")
else:
    st.info("⏸ Le bot est inactif. Activez-le pour lancer l’analyse.")

st.write("---")
st.write("### 📊 Statistiques de gestion du risque")

stats = st.session_state.trade_manager.get_stats()
col1, col2, col3 = st.columns(3)
col1.metric("💰 Capital", f"{stats['capital']} $")
col2.metric("📈 Trades aujourd’hui", stats["trades_today"])
col3.metric("❌ Pertes aujourd’hui", stats["losses_today"])

col4, col5 = st.columns(2)
col4.metric("🔥 Série de gains", stats["win_chain"])
col5.metric("⚙️ Risque par trade", f"{stats['risk_per_trade'] * 100:.1f} %")
