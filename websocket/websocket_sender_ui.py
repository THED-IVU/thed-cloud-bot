
import streamlit as st
import asyncio
import websockets
import json
from datetime import datetime

st.set_page_config(page_title="🧪 Envoi manuel de signaux IA", layout="centered")
st.title("📤 Simulateur d'envoi de signaux IA vers WebSocket")

symbol = st.selectbox("📈 Actif", ["EURUSD", "BTCUSD", "ETHUSD", "USDJPY"])
direction = st.selectbox("📊 Direction IA", ["UP", "DOWN"])
score = st.slider("🎯 Score IA (%)", 50, 100, 75)
contexte = st.selectbox("📚 Contexte marché", ["Range", "Expansion", "Retournement"])
mise = st.slider("💰 Mise ($)", 1, 100, 5)
duree = st.selectbox("⏱️ Durée (sec)", [30, 60, 120])
resume_technique = st.text_input("📈 Résumé technique", "RSI=70, EMA croisée haussière")
resume_fondamentale = st.text_input("📰 Résumé fondamental", "Pas de nouvelle majeure")

async def send_trade_signal():
    uri = "ws://localhost:8765"
    signal = {
        "timestamp": datetime.now().isoformat(),
        "symbol": symbol,
        "direction": direction,
        "score": score,
        "contexte": contexte,
        "mise": mise,
        "duree": duree,
        "resume_technique": resume_technique,
        "resume_fondamentale": resume_fondamentale
    }
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(signal))
            st.success("✅ Signal envoyé avec succès")
    except Exception as e:
        st.error(f"❌ Erreur WebSocket : {e}")

if st.button("📤 Envoyer le signal"):
    asyncio.run(send_trade_signal())
