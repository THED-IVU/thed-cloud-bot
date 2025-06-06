
import streamlit as st
import pandas as pd
import time
import os
import json
import firebase_admin
from firebase_admin import credentials, db

# Initialisation Firebase
if not firebase_admin._apps:
    cred_path = os.path.join("firebase", "firebase_config.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://your-project-id.firebaseio.com/'  # Remplacer par votre URL
        })
    else:
        st.error("❌ Fichier de configuration Firebase manquant.")
        st.stop()

st.set_page_config(page_title="📡 Suivi IA - Firebase", layout="wide")
st.title("📡 Suivi des Signaux IA - Firebase (Temps Réel)")

# Auto-refresh toutes les 10 secondes
st_autorefresh = st.empty()
count = st_autorefresh.empty()
count.write("🔄 Rafraîchissement automatique toutes les 10 secondes...")

time.sleep(10)
count.empty()

ref = db.reference("signals")
data = ref.get()

if not data:
    st.warning("⚠️ Aucun signal trouvé dans Firebase.")
    st.stop()

df = pd.DataFrame(data.values())

# Filtres
actifs = df["symbol"].unique().tolist()
symbol_filter = st.selectbox("🎯 Filtrer par actif :", ["Tous"] + actifs)
score_min = st.slider("📊 Score IA minimum :", 0, 100, 50)

if symbol_filter != "Tous":
    df = df[df["symbol"] == symbol_filter]

df = df[df["score"].astype(float) >= score_min]

# Affichage
st.dataframe(df)

# Export CSV
export_btn = st.button("📥 Exporter en CSV")
if export_btn:
    csv_path = "firebase_signaux_export.csv"
    df.to_csv(csv_path, index=False)
    with open(csv_path, "rb") as f:
        b64 = f.read()
    st.download_button("⬇️ Télécharger le CSV", b64, file_name="firebase_signaux_export.csv")
