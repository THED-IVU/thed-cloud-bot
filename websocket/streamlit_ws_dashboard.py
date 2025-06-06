
import streamlit as st
import websocket
import threading
import json
import pandas as pd

st.set_page_config(page_title="🛰️ Dashboard IA Temps Réel", layout="wide")
st.title("📡 Suivi Temps Réel des Signaux IA")

placeholder = st.empty()
log_data = []

def on_message(ws, message):
    data = json.loads(message)
    log_data.append(data)
    df = pd.DataFrame(log_data)
    with placeholder.container():
        st.subheader("📊 Signaux Reçus")
        st.dataframe(df[::-1], use_container_width=True)

def on_error(ws, error):
    st.error(f"❌ Erreur WebSocket : {error}")

def on_close(ws, close_status_code, close_msg):
    st.warning("🔌 Connexion WebSocket fermée.")

def on_open(ws):
    st.success("✅ Connexion WebSocket établie.")
    # Peut être utilisé pour envoyer un message d'initiation
    ws.send(json.dumps({"status": "Client Streamlit prêt"}))

# Lancer le WebSocket dans un thread séparé
def run_ws():
    ws = websocket.WebSocketApp(
        "ws://localhost:5678",  # Adresse locale de realtime_server.py
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

thread = threading.Thread(target=run_ws)
thread.start()


# 🔥 Bloc Firebase intégré automatiquement

    st.markdown("## 🔥 Historique Firebase (Derniers trades enregistrés)")
    try:
        from firebase_admin import credentials, firestore, initialize_app
        if "firebase_app" not in st.session_state:
            cred = credentials.Certificate("firebase_credentials.json")
            st.session_state.firebase_app = initialize_app(cred)
        db = firestore.client()
        trades_ref = db.collection("trades").order_by("datetime", direction=firestore.Query.DESCENDING).limit(10)
        docs = trades_ref.stream()
        for doc in docs:
            data = doc.to_dict()
            st.write(f"{data['datetime']} | {data['symbol']} | {data['direction']} | Score : {data['confiance']}%")
    except Exception as e:
        st.warning(f"⚠️ Firebase non connecté ou erreur : {e}")
