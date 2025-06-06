
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

st.set_page_config(page_title="📡 Live Bot IA Cloud", layout="wide")
st.title("🧠 Bot IA – Exécution Live (Render Cloud WebSocket)")

symbol = st.sidebar.selectbox("📈 Actif", ["EURUSD", "BTCUSD", "USDJPY", "XAUUSD"], index=0)
use_ai = st.sidebar.checkbox("🤖 Activer IA", value=True)
capital = st.sidebar.number_input("💰 Capital", value=1000, step=100)

if "trade_manager" not in st.session_state:
    st.session_state.trade_manager = TradeManager(capital=capital)

prix = get_prix_reel(symbol)
if prix:
    st.markdown("### 💹 Prix actuel (%s) : `%0.5f`" % (symbol, prix))
    for msg in cloture_auto_si_tp_sl(symbol, prix):
        st.warning(msg)
else:
    st.error("❌ Prix indisponible")

async def websocket_cloud():
    uri = "wss://tib-ws-ia.onrender.com"
    async with websockets.connect(uri) as websocket:
        st.sidebar.success("🔗 Connecté à Render WebSocket")
        while True:
            message = await websocket.recv()
            signal = json.loads(message)
            st.sidebar.info("⚡ Signal reçu : %s / %s" % (signal.get("symbol", "?"), signal.get("direction", "?")))
            decision, result = run_bot(signal.get("symbol", symbol), use_ai, st.session_state.trade_manager)
            st.sidebar.success("✅ Résultat : %s / %s" % (decision, result))

def lancer_ws():
    asyncio.run(websocket_cloud())

if "ws_cloud" not in st.session_state:
    threading.Thread(target=lancer_ws, daemon=True).start()
    st.session_state.ws_cloud = True

with st.expander("📜 Signaux récents"):
    try:
        with open("logs/ia_signals.log", "r", encoding="utf-8") as f:
            logs = [eval(l) for l in f.readlines() if symbol in l][-10:]
            df = pd.DataFrame(logs)
            df["datetime"] = pd.to_datetime(df["datetime"])
            st.dataframe(df.sort_values("datetime", ascending=False))
    except:
        st.info("Aucun log trouvé.")
