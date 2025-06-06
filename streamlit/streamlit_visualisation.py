
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Visualisation des Trades IA", layout="wide")

# 🔐 Authentification simple
PASSWORD = "19876Slymthed@"
if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = False

if not st.session_state.auth_ok:
    mdp = st.text_input("🔐 Entrez le mot de passe :", type="password")
    if mdp == PASSWORD:
        st.session_state.auth_ok = True
        st.success("✅ Accès autorisé")
    else:
        st.stop()

# Connexion à la base
DB_PATH = "trades.db"

def charger_trades():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM trades ORDER BY timestamp DESC", conn)
    conn.close()
    return df

# 📊 Choix du type de visualisation
st.sidebar.header("🎛️ Options")
mode = st.sidebar.selectbox("🎯 Type de Trading", ["Binaire", "Forex"])
graph_type = st.sidebar.radio("📈 Type de graphique", ["Score", "Volume"])

df = charger_trades()

if df.empty:
    st.warning("⚠️ Aucun trade enregistré pour l’instant.")
    st.stop()

st.markdown(f"### 📋 Historique des trades ({mode}) – {len(df)} lignes")

# 📊 Graphique
st.subheader("📊 Visualisation Graphique")
if graph_type == "Score":
    fig, ax = plt.subplots()
    df["score"] = df["score"].astype(float)
    df.plot(x="timestamp", y="score", kind="line", ax=ax, title="Évolution des Scores IA")
    st.pyplot(fig)
else:
    fig, ax = plt.subplots()
    df["mise"] = df["mise"].astype(int)
    df.groupby("symbol")["mise"].sum().plot(kind="bar", ax=ax, title="Volume de Mise par Actif")
    st.pyplot(fig)

# 🧾 Tableau brut
with st.expander("📄 Voir les données brutes"):
    st.dataframe(df)
