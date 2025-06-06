# 📄 streamlit/pages/4_IA_Learning_Center.py

import streamlit as st
import pandas as pd
from core.learning_tracker import (
    load_learning_data,
    save_learning_data,
    update_learning_from_history
)
from db import lire_trades

st.set_page_config(page_title="Centre IA Adaptatif", layout="wide")
st.title("🧠 Centre d'apprentissage IA du bot")

# 🔄 Rafraîchir les données depuis l’historique
if st.button("🔁 Apprentissage automatique depuis l'historique"):
    result = update_learning_from_history()
    st.success("🎯 Mise à jour des poids IA / techniques réussie.")

# 📥 Données actuelles
data = load_learning_data()
strategies = data.get("strategies", {})

# 📊 Aperçu des stats par stratégie
st.subheader("📈 Statistiques par stratégie")
if strategies:
    df = pd.DataFrame(strategies).T
    df.index.name = "stratégie"
    st.dataframe(df.style.format(precision=2), use_container_width=True)
else:
    st.warning("Aucune donnée d'historique enregistrée pour l’instant.")

# 🎚 Ajustements manuels
st.markdown("### ⚙️ Réglages IA / Technique")
col1, col2 = st.columns(2)
with col1:
    new_ia = st.slider("Poids IA", min_value=0.1, max_value=3.0, value=float(data["ia_validation_weight"]), step=0.1)
with col2:
    new_tech = st.slider("Poids technique", min_value=0.1, max_value=3.0, value=float(data["technique_weight"]), step=0.1)

new_threshold = st.slider("Seuil global minimum (score)", min_value=0, max_value=100, value=int(data["global_score_threshold"]))

# ✅ Enregistrement
if st.button("💾 Enregistrer les réglages manuels"):
    data["ia_validation_weight"] = new_ia
    data["technique_weight"] = new_tech
    data["global_score_threshold"] = new_threshold
    save_learning_data(data)
    st.success("✅ Réglages enregistrés avec succès.")

# 🕹 Données brutes (facultatif)
with st.expander("🧪 Données brutes (JSON learning_data.json)"):
    st.json(data)
