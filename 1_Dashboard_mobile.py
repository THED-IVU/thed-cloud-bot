import streamlit as st
from datetime import datetime

st.set_page_config(page_title="📱 THED BOT – Mobile", layout="wide")

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    .css-18e3th9 {
        padding-top: 1rem;
    }
    .stButton>button {
        font-size: 18px;
        padding: 0.75em 1.5em;
    }
    .stSelectbox>div {
        font-size: 18px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 THED BOT – Mobile")

menu = st.selectbox("📋 Menu", [
    "Dashboard IA",
    "Prédictions + Patterns",
    "Historique",
    "Rapport rapide",
    "Configuration IA"
])

if menu == "Dashboard IA":
    st.switch_page("pages/2_Dashboard_IA.py")

elif menu == "Prédictions + Patterns":
    st.switch_page("pages/Dashboard_IA_Resultats.py")

elif menu == "Historique":
    st.switch_page("pages/historique_ia_patterns.py")

elif menu == "Rapport rapide":
    st.switch_page("pages/Rapport_IA.py")

elif menu == "Configuration IA":
    st.switch_page("pages/Admin_IA_Config.py")

st.markdown("---")
st.caption("📱 Interface optimisée mobile – THED IVU BOT")