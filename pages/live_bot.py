
import streamlit as st
import pandas as pd
import asyncio
import threading
import websockets
import json
from datetime import datetime
from core.core_bot import run_bot
from core.forex_manager import cloture_auto_si_tp_sl
from core.init_mt5_connection import get_prix_reel
from core.risk_manager import TradeManager

# ⚙️ Configuration générale
st.set_page_config(page_title="📡 Live Bot IA", layout="wide")
st.title("🧠 Bot IA – Exécution Live et Suivi des Trades")

# 🔧 Paramètres utilisateur
st.sidebar.header("⚙️ Paramètres de trading")
symbol = st.sidebar.selectbox("📈 Actif à analyser", ["EURUSD", "BTCUSD", "USDJPY", "XAUUSD"], index=0)
use_ai = st.sidebar.checkbox("🤖 Utiliser l’IA pour décider ?", value=True)
capital_initial = st.sidebar.number_input("💰 Capital initial", value=1000, step=100)

# Stocker le TradeManager en session
if "trade_manager" not in st.session_state:
    st.session_state.trade_manager = TradeManager(capital=capital_initial)

# 📉 Récupération du prix réel MT5
prix_actuel = get_prix_reel(symbol)
if prix_actuel:
    st.markdown(f"### 💹 Prix actuel ({symbol}) : `{prix_actuel:.5f}`")
else:
    st.error(f"❌ Impossible de récupérer le prix actuel pour {symbol} via MT5.")

# 🔁 Vérification automatique des TP/SL
if prix_actuel:
    messages = cloture_auto_si_tp_sl(symbol, prix_actuel)
    if messages:
        st.subheader("🛑 Clôtures automatiques détectées")
        for msg in messages:
            st.warning(msg)

# 🚀 Bouton de lancement IA
exec_now = st.sidebar.button("🚀 Lancer un cycle IA maintenant")

if exec_now:
    with st.spinner("🔄 Analyse en cours..."):
        decision, resultat = run_bot(symbol, use_ai, trade_manager=st.session_state.trade_manager)
    st.success(f"✅ {symbol} | Décision : {decision.upper()} | Résultat : {resultat}")

# ✅ WebSocket – exécution automatique sur réception
async def websocket_listener():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        st.sidebar.success("🔗 WebSocket connecté")
        while True:
            message = await websocket.recv()
            signal = json.loads(message)
            st.sidebar.warning(f"🧠 Signal reçu via WebSocket : {signal.get('symbol', '??')}")

            if "symbol" in signal:
                decision, result = run_bot(signal["symbol"], use_ai=True, trade_manager=st.session_state.trade_manager)
                st.sidebar.success(f"✅ Signal exécuté ({signal['symbol']}) : {decision} – {result}")

def start_websocket():
    asyncio.run(websocket_listener())

if "ws_started" not in st.session_state:
    threading.Thread(target=start_websocket, daemon=True).start()
    st.session_state.ws_started = True

# 📜 Logs récents
with st.expander("📜 Derniers signaux IA enregistrés"):
    try:
        with open("logs/ia_signals.log", "r", encoding="utf-8") as f:
            lignes = f.readlines()
        lignes_filtrees = [l for l in lignes if symbol in l]
        if lignes_filtrees:
            logs_dict = [eval(l) for l in lignes_filtrees[-10:]]
            df = pd.DataFrame(logs_dict)
            df["datetime"] = pd.to_datetime(df["datetime"])
            st.dataframe(df.sort_values(by="datetime", ascending=False), use_container_width=True)
        else:
            st.info("Aucun signal trouvé pour cet actif.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture des logs : {e}")

# 🧪 Debug
with st.expander("🧪 Mode développeur / debug IA"):
    st.code(f"Actif : {symbol}\nIA activée : {use_ai}\nPrix actuel (MT5) : {prix_actuel}")
