# pages/13_Explorateur_Analyses_IA.py

import streamlit as st
import sqlite3
import pandas as pd
import os
import json

DB_PATH = os.getenv("LOCAL_DB_PATH", "MON_API_PRO/ia_analysis.db")

st.set_page_config(page_title="📂 Explorateur IA", layout="wide")
st.title("📂 Explorateur des Analyses IA Sauvegardées")

# 🔍 Fonction pour charger les analyses
def charger_analyses():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame(columns=["id", "type", "horodatage", "contenu"])

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM analyses ORDER BY horodatage DESC", conn)
    conn.close()

    # Parser le JSON
    def parse_json(row):
        try:
            return json.loads(row)
        except:
            return {"Erreur": "JSON invalide"}

    df["contenu_json"] = df["contenu"].apply(parse_json)
    return df

# 📦 Chargement
df = charger_analyses()

# 🔘 Filtres
with st.expander("🔧 Filtres et options", expanded=True):
    types_disponibles = df["type"].unique().tolist()
    type_filtre = st.multiselect("Type d’analyse", types_disponibles, default=types_disponibles)
    date_min = st.date_input("Date min", value=None)
    date_max = st.date_input("Date max", value=None)

# 🎯 Application des filtres
if type_filtre:
    df = df[df["type"].isin(type_filtre)]

if date_min:
    df = df[df["horodatage"] >= str(date_min)]

if date_max:
    df = df[df["horodatage"] <= str(date_max)]

# 📊 Affichage des données
st.subheader(f"🧾 {len(df)} analyse(s) trouvée(s)")
for _, row in df.iterrows():
    with st.expander(f"🗓 {row['horodatage']} – {row['type']}"):
        st.json(row["contenu_json"])

# 📤 Export
st.divider()
st.subheader("📤 Exporter les résultats")

col1, col2 = st.columns(2)

with col1:
    if st.button("📄 Export CSV"):
        export_df = df[["type", "horodatage", "contenu"]]
        csv = export_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Télécharger CSV", csv, "analyses_ia.csv", "text/csv")

with col2:
    if st.button("🧾 Export JSON"):
        json_data = df[["type", "horodatage", "contenu_json"]].to_dict(orient="records")
        json_str = json.dumps(json_data, indent=2, ensure_ascii=False)
        st.download_button("⬇️ Télécharger JSON", json_str, "analyses_ia.json", "application/json")
