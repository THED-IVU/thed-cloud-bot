import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

DATA_FILE = "learning_data/historique_ia.json"

st.set_page_config(page_title="📊 Historique des Trades IA", layout="wide")
st.title("📈 Tableau Historique des Signaux IA")

# Chargement des données
if not os.path.exists(DATA_FILE):
    st.warning("Aucun trade enregistré pour le moment.")
    st.stop()

with open(DATA_FILE, "r", encoding="utf-8") as f:
    try:
        data = json.load(f)
    except json.JSONDecodeError:
        st.error("Erreur de lecture du fichier JSON.")
        st.stop()

if not data:
    st.info("Le fichier est vide pour le moment.")
    st.stop()

# Affichage dans un DataFrame
df = pd.DataFrame(data)
df = df.sort_values(by="timestamp", ascending=False)

# Filtres Streamlit
col1, col2 = st.columns(2)
with col1:
    actif_filtre = st.selectbox("📍 Filtrer par actif", options=["Tous"] + sorted(df["symbole"].unique()))
with col2:
    strategie_filtre = st.selectbox("📊 Filtrer par stratégie", options=["Toutes"] + sorted(df["strategie"].unique()))

if actif_filtre != "Tous":
    df = df[df["symbole"] == actif_filtre]
if strategie_filtre != "Toutes":
    df = df[df["strategie"] == strategie_filtre]

# Affichage
st.markdown(f"### 🔎 {len(df)} signaux IA enregistrés")
st.dataframe(df, use_container_width=True)

# Export CSV
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger CSV", csv, "historique_trades.csv", "text/csv")
