# 📄 streamlit/pages/3_Backtest_Viewer.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import datetime

st.set_page_config(page_title="📁 Historique Backtest", layout="wide")
st.title("📊 Visualiseur des résultats de Backtest")

# -- Mode de chargement
source = st.radio("📦 Source des données :", ["SQLite (db/trades.db)", "CSV (tests/resultats_backtest_multi.csv)"])

# -- Chargement des données
@st.cache_data
def charger_donnees(source):
    if "SQLite" in source:
        conn = sqlite3.connect("db/trades.db")
        df = pd.read_sql_query("SELECT * FROM trades", conn)
        conn.close()
    else:
        df = pd.read_csv("tests/resultats_backtest_multi.csv")

    df["datetime"] = pd.to_datetime(df["datetime"])
    return df

df = charger_donnees(source)

if df.empty:
    st.warning("Aucune donnée trouvée.")
    st.stop()

# -- Filtres
st.sidebar.header("🧰 Filtres")
strategies = df["source"].unique().tolist()
assets = df["asset"].unique().tolist()

selected_strats = st.sidebar.multiselect("🎯 Stratégies", strategies, default=strategies)
selected_assets = st.sidebar.multiselect("📈 Actifs", assets, default=assets)
min_score = st.sidebar.slider("📊 Score minimum", 0, 100, 70)

# -- Application des filtres
df_filtered = df[
    (df["source"].isin(selected_strats)) &
    (df["asset"].isin(selected_assets)) &
    (df["note"] >= min_score)
].copy()

# -- Statistiques globales
st.subheader("🧾 Résumé des signaux filtrés")
col1, col2, col3 = st.columns(3)
col1.metric("📊 Nombre de signaux", len(df_filtered))
col2.metric("💵 Profit total estimé", f"{df_filtered['profit'].sum():.2f} $")
col3.metric("🎯 Score moyen", f"{df_filtered['note'].mean():.1f}")

# -- Table
with st.expander("📄 Détails des signaux"):
    st.dataframe(df_filtered.sort_values("datetime", ascending=False), use_container_width=True)

# -- Graphique : capital simulé
st.subheader("📈 Évolution du capital simulé")

df_filtered = df_filtered.sort_values("datetime")
capital_init = 1000
df_filtered["capital"] = df_filtered["profit"].cumsum() + capital_init

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df_filtered["datetime"], df_filtered["capital"], marker="o", color="green", label="Capital simulé")
ax.set_title("💸 Capital estimé dans le temps")
ax.set_ylabel("Capital ($)")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# -- Histogramme par stratégie
st.subheader("🧠 Performances par stratégie")
strat_stats = df_filtered.groupby("source").agg(
    Nb_signaux=("action", "count"),
    Gain_total=("profit", "sum"),
    Score_moyen=("note", "mean")
)

st.dataframe(strat_stats, use_container_width=True)

# -- Export
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("📥 Télécharger les résultats filtrés (CSV)", csv, file_name="resultats_backtest_filtrés.csv", mime="text/csv")
