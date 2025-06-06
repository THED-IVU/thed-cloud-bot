import streamlit as st
from trading import afficher_statistiques, ajustement_auto, load_params
from utils_ui import init_page
CONFIG = init_page("🤖 Exécution Automatique")

st.title("📊 Tableau de bord - IA Scalping Bot")

params = load_params()
afficher_statistiques()
ajustement_auto(params)
