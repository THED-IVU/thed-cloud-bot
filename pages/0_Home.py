 # 📄 0_Home.py – Page d'accueil du bot IA
import streamlit as st
from datetime import datetime
import os
import json
import requests

from ia_alerts import envoyer_alerte_ia
from ia_storage import sauvegarder_analyse, sync_to_firebase

st.set_page_config(page_title="🏠 Accueil – Bot IA", layout="wide")
st.title("🏠 Bienvenue dans le THED_IVU_BOT")

st.markdown("### 🧭 Utilise le menu à gauche pour naviguer entre les modules disponibles.")

# --- 1. 🔁 Bouton test global ---
st.markdown("---")
st.markdown("## 🧪 Test rapide des fonctions IA")

if st.button("🚀 Lancer test global IA (alerte + Firebase + SQLite)"):
    try:
        resultat_test = {
            "horodatage": datetime.now().isoformat(),
            "source": "test_home",
            "marche": "BTCUSD",
            "horizon": "30min",
            "niveau": "expert",
            "prediction": "Hausse probable à court terme",
            "recommandation": "Acheter au-dessus de 67 500$",
            "score_confiance": 93
        }
        envoyer_alerte_ia(resultat_test)
        sauvegarder_analyse("test_home", resultat_test)
        sync_to_firebase("test_home", resultat_test)
        st.success("✅ Test IA complet effectué depuis la page d'accueil.")
    except Exception as e:
        st.error(f"❌ Erreur pendant le test IA : {e}")

# --- 2. 🔁 Bouton exécution réelle IA ---
st.markdown("## 🤖 Exécuter une vraie analyse IA")

if st.button("🧠 Lancer analyse stratégique réelle"):
    try:
        params = {
            "marche": "forex",
            "horizon": "1j",
            "niveau": "professionnel"
        }
        response = requests.get("http://localhost:8000/analyse_strategique", params=params)
        data = response.json()
        if "resultat" in data:
            st.success("✅ Analyse stratégique reçue.")
            st.json(data["resultat"])
        else:
            st.warning("⚠️ Résultat inattendu.")
            st.write(data)
    except Exception as e:
        st.error(f"❌ Erreur lors de l'appel à l'API locale : {e}")

# --- 3. 📊 Journal des tests précédents ---
st.markdown("## 📋 Journal des tests IA passés")

log_path = "logs/guardian_synced.log"
if os.path.exists(log_path):
    with open(log_path, "r", encoding="utf-8") as f:
        lignes = f.readlines()[-5:]
    for ligne in reversed(lignes):
        try:
            st.code(ligne.strip())
        except:
            st.warning("Ligne illisible ou vide.")
else:
    st.info("Aucun journal trouvé. Lance un test pour initier le log.")

# --- 4. 📱 Mode simplifié pour mobile ---
st.markdown("---")
st.markdown("## 📱 Mode Mobile simplifié")

with st.expander("🔄 Affichage ultra-léger pour mobile/tablette"):
    col1, col2 = st.columns(2)
    col1.button("Analyse IA")
    col2.button("Derniers signaux")

    st.markdown("""
    *Ce mode permet de déclencher les fonctions essentielles même avec une connexion lente ou écran réduit.*
    > Astuce : Ajoute cette page à ton écran d'accueil pour l’utiliser comme une **PWA mobile**.
    """)

# --- Footer ---
st.markdown("---")
st.caption("🧠 THED_IVU_BOT – Interface d’accueil rapide, multi-usage.")
