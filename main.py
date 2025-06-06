# 📄 main.py – Point d'entrée pour l'app IA multipage avec Flask + Sync + Analyse IA

import os
import json
import requests
import threading
from flask import Flask, request, jsonify
from datetime import datetime
from dotenv import load_dotenv

# 🔁 Chargement .env (chemin absolu adapté)
load_dotenv("D:/DOCUMENTATION/PROFESSIONNEL/2025/MES PRODUITS 2025 A VENDRE/TRADING THED/BOT_MT5_THED_PRO_FINAL_CORRECTED/THED/.env")

# === 🔑 API Keys & IA
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
FALLBACK_MODE = os.getenv("PREFERED_AI_FALLBACK", "openai").lower()

# === 🌍 Flask App ===
app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "🤖 API IA stratégique de trading – MON_API_PRO est active."})

@app.route("/analyse_strategique", methods=["GET"])
def analyse_strategique():
    from ia_strategique import analyser_contexte
    marche = request.args.get("marche", "forex")
    horizon = request.args.get("horizon", "1j")
    niveau = request.args.get("niveau", "professionnel")
    try:
        resultat = analyser_contexte(marche=marche, horizon=horizon, niveau=niveau)
        return jsonify({"source": "ia_locale", "resultat": resultat})
    except Exception as e:
        print(f"[❌ IA locale] Erreur détectée : {e}")
        return fallback_ia_cloud(marche, horizon, niveau)

@app.route("/actualites_fondamentales", methods=["GET"])
def actualites_fondamentales():
    from web_crawler_fondamental import recuperer_actualites_economiques
    pays = request.args.get("pays", "us")
    mots_cles = request.args.get("mots_cles", "federal reserve")
    max_articles = int(request.args.get("max_articles", 5))
    actualites = recuperer_actualites_economiques(pays=pays, mots_cles=mots_cles, max_articles=max_articles)
    return jsonify(actualites)

@app.route("/sync", methods=["POST"])
def sync_logs():
    data = request.form.get("logs")
    os.makedirs("logs", exist_ok=True)
    with open("logs/guardian_synced.log", "a", encoding="utf-8") as f:
        f.write(data + "\n")
    return jsonify({"status": "received"}), 200

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# === 🧠 Fallback IA Cloud ===
def fallback_ia_cloud(marche, horizon, niveau):
    if FALLBACK_MODE == "openai":
        return fallback_openai(marche, horizon, niveau)
    elif FALLBACK_MODE == "gemini":
        return fallback_gemini(marche, horizon, niveau)
    else:
        return jsonify({"source": "fallback_indisponible", "erreur": f"⚠️ Fallback inconnu : {FALLBACK_MODE}"})


# === 🔁 Fallback OpenAI ===
def fallback_openai(marche, horizon, niveau):
    prompt = f"""
Tu es un expert en stratégie de marché comme Warren Buffett et George Soros.
Analyse le marché {marche.upper()} à horizon {horizon} pour un niveau {niveau}.
Donne une prédiction, une tendance probable, une recommandation stratégique.
Réponds en JSON structuré avec : horodatage, source, marche, horizon, niveau, prediction, recommandation, score_confiance
"""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "Tu es un analyste stratégique financier expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        text = response.json()['choices'][0]['message']['content']
        return jsonify({"source": "openai", "resultat": json.loads(text)})
    except Exception as e:
        return jsonify({"source": "openai", "erreur": f"Erreur OpenAI : {e}"})


# === 🔁 Fallback Gemini ===
def fallback_gemini(marche, horizon, niveau):
    prompt = {
        "contents": [{
            "parts": [{
                "text": f"Analyse le marché {marche} à horizon {horizon}, niveau {niveau}. Donne des insights pro au format JSON structuré."
            }]
        }]
    }
    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=prompt
        )
        text = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"source": "gemini", "resultat": json.loads(text)})
    except Exception as e:
        return jsonify({"source": "gemini", "erreur": f"Erreur Gemini : {e}"})


# === 🚀 Lancement Streamlit + Flask ensemble ===

threading.Thread(target=run_flask, daemon=True).start()

# ⬇️ Partie Streamlit (interface)
import streamlit as st
from config_state import sidebar_config, get_runtime_config
from core.firebase_logger import envoyer_log_firebase

st.set_page_config(page_title="Bot IA Multipage", layout="wide")
st.title("🤖 Exécution Automatique")

sidebar_config()
CONFIG = get_runtime_config()

st.sidebar.title("🧭 Navigation IA stratégique")
st.sidebar.page_link("pages/1_Dashboard.py", label="📊 Dashboard Principal")
st.sidebar.page_link("pages/2_Trading_Auto.py", label="🤖 Bot Trading Automatique")
st.sidebar.page_link("pages/12_Analyse_IA_Strategique.py", label="🧠 Analyse IA Stratégique")
st.sidebar.page_link("pages/13_Explorateur_Analyses_IA.py", label="📂 Historique Analyses IA")

# 🔄 Firebase Manual Sync
st.sidebar.markdown("### ☁️ Firebase Sync")
if st.sidebar.button("🔄 Synchroniser maintenant"):
    from firebase_sync import synchroniser_firebase
    res = synchroniser_firebase()
    st.sidebar.success(res if "✅" in res else res)

# 🧠 Indication IA
if CONFIG["use_ai"]:
    modele = CONFIG[CONFIG["ai_provider"]].get("model", "modèle inconnu")
    st.success(f"🧠 IA activée avec : **{CONFIG['ai_provider'].upper()}**\n\nModèle : `{modele}`")
else:
    st.info("⚙️ Mode TECHNIQUE uniquement (IA désactivée)")

# Exemple d'action loggée
envoyer_log_firebase(
    plateforme="MT5",
    action="Backtest terminé",
    resultat="gagné",
    strategie="EMA_RSI"
)
