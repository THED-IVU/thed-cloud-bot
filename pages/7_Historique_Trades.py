import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---------------------------
# CONFIGURATION INITIALE
# ---------------------------
DB_PATH = "trades.db"
PASSWORD = "admin"

# ---------------------------
# FONCTIONS UTILES
# ---------------------------
def load_trades():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM trades ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def filtrer_par_mode(df, mode):
    if mode == "binaire":
        return df[df.symbol.isin(["BTCUSD", "ETHUSD"])]
    elif mode == "forex":
        return df[~df.symbol.isin(["BTCUSD", "ETHUSD"])]
    return df  # tous

# ---------------------------
# AUTHENTIFICATION
# ---------------------------
st.set_page_config(page_title="Historique des Trades", layout="wide")
st.title("📊 Historique des Trades enregistrés")

mdp = st.text_input("Mot de passe", type="password")
if mdp != PASSWORD:
    st.warning("Accès restreint. Veuillez entrer le mot de passe correct.")
    st.stop()

# ---------------------------
# FILTRAGE & AFFICHAGE
# ---------------------------
df = load_trades()
mode = st.selectbox("Sélectionnez le mode de trading", ["tous", "binaire", "forex"])
df_filtre = filtrer_par_mode(df, mode)

# ---------------------------
# TABLEAU INTERACTIF
# ---------------------------
st.subheader("🧾 Tableau des trades")
st.dataframe(df_filtre, use_container_width=True)

# ---------------------------
# GRAPHIQUE
# ---------------------------
st.subheader("📈 Visualisation graphique")
graphe = st.radio("Type de graphique", ["Scores", "Mises"], horizontal=True)

fig, ax = plt.subplots()
if graphe == "Scores":
    df_filtre.plot(kind="bar", x="timestamp", y="score", ax=ax, legend=False)
    ax.set_ylabel("Score")
else:
    df_filtre.plot(kind="bar", x="timestamp", y="mise", ax=ax, color="orange", legend=False)
    ax.set_ylabel("Mise")
plt.xticks(rotation=45)
st.pyplot(fig)

# ---------------------------
# INFO SUPPLÉMENTAIRE
# ---------------------------
st.markdown("""
<style>
    section[data-testid="stSidebar"] > div:first-child {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)
