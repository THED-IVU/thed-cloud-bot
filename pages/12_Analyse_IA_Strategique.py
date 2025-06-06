# pages/12_Analyse_IA_Strategique.py

import streamlit as st
import requests
import datetime
import json
import os

# 📦 Optionnel : import du module de stockage
try:
    from ia_storage import sauvegarder_analyse_locale, sync_to_firebase
except:
    sauvegarder_analyse_locale = None
    sync_to_firebase = None

# 🌐 Configuration API (à adapter selon déploiement local/Render)
API_URL = os.getenv("API_URL", "http://localhost:8000")

# === Configuration de la page
st.set_page_config(page_title="🧠 Analyse IA Stratégique", layout="wide")
st.title("🧠 Analyse IA Stratégique et Fondamentale")
st.markdown("Déclenche une analyse stratégique via ton moteur IA local ou cloud.")

# === SECTION 1 — ANALYSE STRATÉGIQUE
st.subheader("📊 Analyse Stratégique")
col1, col2, col3 = st.columns(3)

marche = col1.selectbox("📈 Marché", ["forex", "crypto", "indices", "actions"])
horizon = col2.selectbox("⏳ Horizon", ["1h", "4h", "1j", "1s", "1m"])
niveau = col3.selectbox("📊 Niveau d'analyse", ["amateur", "intermédiaire", "professionnel"])

if st.button("🚀 Lancer l’analyse stratégique"):
    try:
        res = requests.get(f"{API_URL}/analyse_strategique", params={
            "marche": marche,
            "horizon": horizon,
            "niveau": niveau
        })
        if res.status_code == 200:
            data = res.json()
            st.success(f"✅ Analyse IA reçue depuis : `{data.get('source', 'inconnue')}`")
            st.json(data.get("resultat", data))

            # 🧠 Sauvegarde automatique locale
            if sauvegarder_analyse_locale:
                sauvegarder_analyse_locale("strategique", data)

            # 🔄 Sync Firebase si dispo
            if sync_to_firebase:
                sync_to_firebase("strategique", data)

        else:
            st.error(f"❌ Erreur : {res.text}")
    except Exception as e:
        st.error(f"❌ Erreur d’accès à l’API : {e}")

st.divider()

# === SECTION 2 — ANALYSE FONDAMENTALE
st.subheader("🌐 Analyse Fondamentale (Actualités)")
col4, col5 = st.columns(2)

pays = col4.text_input("🌍 Pays ciblé", value="us")
mots_cles = col5.text_input("🧠 Mots-clés de recherche", value="federal reserve")
max_articles = st.slider("📰 Nombre d'articles", 1, 10, value=5)

if st.button("🔍 Récupérer les actualités fondamentales"):
    try:
        res = requests.get(f"{API_URL}/actualites_fondamentales", params={
            "pays": pays,
            "mots_cles": mots_cles,
            "max_articles": max_articles
        })
        if res.status_code == 200:
            news = res.json().get("actualites", [])
            st.success("📰 Actualités récupérées")

            for i, article in enumerate(news, 1):
                st.markdown(f"### {i}. {article.get('titre', 'Sans titre')}")
                st.write(f"🗞 {article.get('source')} – 🕒 {article.get('date')}")
                st.markdown(f"[🔗 Lire l'article]({article.get('url')})", unsafe_allow_html=True)

            if sauvegarder_analyse_locale:
                sauvegarder_analyse_locale("fondamentale", news)

            if sync_to_firebase:
                sync_to_firebase("fondamentale", news)

        else:
            st.error(f"❌ Erreur : {res.text}")
    except Exception as e:
        st.error(f"❌ Erreur d’accès à l’API : {e}")
