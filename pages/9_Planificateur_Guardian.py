
# pages/9_Planificateur_Guardian.py

import streamlit as st
import subprocess
import os
import signal

st.set_page_config(page_title="🕒 Planificateur Guardian", layout="centered")
st.title("🕒 Planificateur automatique Guardian IA")

st.markdown("Ce module permet de **lancer ou arrêter** la surveillance automatique du bot.")

if "process_id" not in st.session_state:
    st.session_state.process_id = None

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Lancer le scan automatique"):
        if st.session_state.process_id is None:
            process = subprocess.Popen(["python", "guardian/guardian_scheduler.py"])
            st.session_state.process_id = process.pid
            st.success(f"✅ Scheduler lancé (PID: {process.pid})")
        else:
            st.warning("⏳ Scheduler déjà en cours d'exécution.")

with col2:
    if st.button("⛔ Arrêter le scan automatique"):
        if st.session_state.process_id:
            try:
                os.kill(st.session_state.process_id, signal.SIGTERM)
                st.success(f"🛑 Processus arrêté (PID: {st.session_state.process_id})")
                st.session_state.process_id = None
            except Exception as e:
                st.error(f"Erreur lors de l'arrêt : {e}")
        else:
            st.info("Aucun processus en cours.")
