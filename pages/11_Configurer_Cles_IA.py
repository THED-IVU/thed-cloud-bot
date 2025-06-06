
# pages/11_Configurer_Cles_IA.py

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="🔐 Clés API IA", layout="centered")
st.title("🔐 Configuration des clés API")

env_path = Path("D:/DOCUMENTATION/PROFESSIONNEL/2025/MES PRODUITS 2025 A VENDRE/TRADING THED/BOT_MT5_THED_PRO_FINAL_CORRECTED/THED/.env")

if not env_path.exists():
    st.warning(f"Fichier .env introuvable à l'emplacement : {env_path}")
else:
    # Lire les lignes existantes
    lignes = env_path.read_text(encoding="utf-8").splitlines()
    cles_existantes = {line.split("=")[0]: line.split("=")[1] for line in lignes if "=" in line}

    st.subheader("🔧 Modifier les clés suivantes :")

    new_openai_key = st.text_input("Clé OpenAI", value=cles_existantes.get("OPENAI_API_KEY", ""))
    new_gemini_key = st.text_input("Clé Gemini", value=cles_existantes.get("GEMINI_API_KEY", ""))
    new_news_key = st.text_input("Clé NewsAPI", value=cles_existantes.get("NEWS_API_KEY", ""))
    new_ia_locale_key = st.text_input("Clé IA Locale", value=cles_existantes.get("LOCAL_IA_KEY", ""))

    if st.button("💾 Enregistrer les modifications"):
        cles_existantes["OPENAI_API_KEY"] = new_openai_key
        cles_existantes["GEMINI_API_KEY"] = new_gemini_key
        cles_existantes["NEWS_API_KEY"] = new_news_key
        cles_existantes["LOCAL_IA_KEY"] = new_ia_locale_key

        contenu_final = "\n".join([f"{k}={v}" for k, v in cles_existantes.items()])
        env_path.write_text(contenu_final, encoding="utf-8")
        st.success("✅ Clés mises à jour avec succès.")
