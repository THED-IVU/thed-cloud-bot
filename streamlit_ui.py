# 📄 streamlit_ui.py - Interface Streamlit principale du bot TIB

import os
import streamlit as st

st.set_page_config(page_title="THED IVU BOT - TIB", layout="wide")

st.title("🤖 THED IVU BOT (TIB)")
st.subheader("Bienvenue dans l'interface principale de votre bot de trading")
st.caption("Choisissez un module dans le menu à gauche")

st.markdown("### 📊 Modules disponibles :")
st.markdown("- `1_Dashboard.py` → Vue d'ensemble")
st.markdown("- `2_Backtest_MultiStrat.py` → Backtest")
st.markdown("- `3_Guardian_Dashboard.py` → TIB Guardian")
st.markdown("- `6_PocketOption_Copilote.py` → Assistant PO navigateur")

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Aller à :", [
    "Dashboard", 
    "Simulation rapide",
    "Backtest",
    "Guardian IA",
    "Pocket Option Copilote"
])

if page == "Dashboard":
    os.system("streamlit run pages/1_Dashboard.py")
elif page == "Simulation rapide":
    os.system("streamlit run streamlit/pages/simulation_rapide.py")
elif page == "Backtest":
    os.system("streamlit run 2_Backtest_MultiStrat.py")
elif page == "Guardian IA":
    os.system("streamlit run guardian_dashboard.py")
elif page == "Pocket Option Copilote":
    os.system("streamlit run 6_PocketOption_Copilote.py")
