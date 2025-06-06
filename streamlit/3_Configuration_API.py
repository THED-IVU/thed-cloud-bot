# 📄 Fichier : streamlit/3_Configuration_API.py

import streamlit as st
from runtime_config import load_config, save_config
from scanner import get_active_assets

st.set_page_config(page_title="Configuration API / IA", layout="wide")
st.title("⚙️ Configuration API IA & Scanner Actifs")

# --------- Configuration IA ---------
config = load_config()

st.subheader("🤖 Paramètres de l'IA")
use_ai = st.checkbox("Activer l'IA", value=config.get("use_ai", True))
model = st.selectbox("Modèle utilisé", ["openai", "gemini", "local"], index=["openai", "gemini", "local"].index(config.get("model", "openai")))
freq_api = st.slider("⏱ Fréquence appel IA (backtest)", 1, 10, value=config.get("api_freq", 3))

# --------- Configuration Scanner ---------
st.subheader("📡 Source d'actifs à scanner")
source = st.radio("Source des actifs", ["auto", "mt5", "hybrid", "yahoo"], index=0)
actifs = get_active_assets(source=source)

st.write(f"🔎 {len(actifs)} actifs détectés :", actifs)

# --------- Sauvegarde ---------
if st.button("💾 Enregistrer les paramètres"):
    config["use_ai"] = use_ai
    config["model"] = model
    config["api_freq"] = freq_api
    config["asset_source"] = source
    save_config(config)
    st.success("✅ Configuration sauvegardée !")
