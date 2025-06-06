
# pages/10_Gestionnaire_Maj_Guardian.py

import streamlit as st
import subprocess
import os
import signal

st.set_page_config(page_title="⚙️ Mises à jour Guardian", layout="centered")
st.title("⚙️ Automatisation des mises à jour Guardian IA")

st.markdown("Active ou désactive les synchronisations automatiques toutes les 6h (structure + GitHub + Firebase).")

if "maj_pid" not in st.session_state:
    st.session_state.maj_pid = None

col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Activer la mise à jour automatique"):
        if st.session_state.maj_pid is None:
            process = subprocess.Popen(["python", "guardian/guardian_updater.py"])
            st.session_state.maj_pid = process.pid
            st.success(f"✅ Processus lancé (PID: {process.pid})")
        else:
            st.warning("⏳ Une mise à jour automatique est déjà en cours.")

with col2:
    if st.button("⛔ Stopper la mise à jour automatique"):
        if st.session_state.maj_pid:
            try:
                os.kill(st.session_state.maj_pid, signal.SIGTERM)
                st.success(f"🛑 Processus arrêté (PID: {st.session_state.maj_pid})")
                st.session_state.maj_pid = None
            except Exception as e:
                st.error(f"Erreur lors de l'arrêt : {e}")
        else:
            st.info("Aucun processus actif.")
