import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Modules internes
from trading import (
    load_params, afficher_parametres_sidebar, init_trade_history,
    afficher_historique, afficher_statistiques,
    ajustement_auto, analyser_retours_trades
)
from scanner import scanner_actifs
from db import initialiser_table
from streamlit_ui import (
    afficher_filtres_sidebar, afficher_table_scan,
    afficher_heatmap, afficher_analyse_actif
)

# 💾 Initialisation de la base de données
initialiser_table()

# ------------------- 1. Initialisation -------------------
st.set_page_config(page_title="Bot de Trading IA", layout="wide")
st_autorefresh(interval=60000, key="refresh")
init_trade_history()
params = load_params()
afficher_parametres_sidebar(params)

# ------------------- 2. Données -------------------
st.title("📈 Bot IA - Scalping Multi-Actifs")
st.info("Chargement des données minute en cours...")

# Filtres dynamiques (refactor UI)
tendance_selection, score_min, affichage_graphique = afficher_filtres_sidebar()

# ------------------- 3. Scanner les actifs -------------------
df_scan = scanner_actifs(params)

# Application des filtres dynamiques
if tendance_selection != "Tous":
    df_scan = df_scan[df_scan["Marché technique"] == tendance_selection]
df_scan = df_scan[df_scan["Score total"] >= score_min]

# ------------------- 4. Affichage UI -------------------
afficher_table_scan(df_scan)
afficher_heatmap(df_scan)

# Sélection de l’actif optimal
if not df_scan.empty:
    meilleur = df_scan.sort_values("Score total", ascending=False).iloc[0]
    if affichage_graphique:
        afficher_analyse_actif(meilleur, params)

# ------------------- 5. Historique & Stats -------------------
st.markdown("---")
afficher_historique()
afficher_statistiques()
analyser_retours_trades()
ajustement_auto(params)
