import os
import json
import openai
import requests
import datetime
from dotenv import load_dotenv

# 🔐 Chargement des variables d'environnement
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOCAL_IA_URL = os.getenv("LOCAL_IA_URL")
IA_KEY = os.getenv("IA_KEY")
FALLBACK_MODE = os.getenv("PREFERED_AI_FALLBACK", "openai").lower()

# 🎯 Analyse stratégique principale avec fallback dynamique
def analyser_contexte(marche="forex", horizon="1j", niveau="professionnel"):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # 🔍 1. Tentative d'utilisation de l'IA locale
        headers = {
            "Authorization": f"Bearer {IA_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "marche": marche,
            "horizon": horizon,
            "niveau": niveau
        }
        response = requests.post(LOCAL_IA_URL, headers=headers, json=payload, timeout=5)

        if response.status_code == 200:
            data = response.json()
            data["source"] = "ia_locale"
            data["horodatage"] = now
            return data
        else:
            print(f"[⚠️ IA Locale] Statut {response.status_code} : {response.text}")
            raise RuntimeError("Échec IA locale")

    except Exception as e:
        print(f"[❌ IA Locale] Erreur : {e}")
        return analyser_contexte_fallback(marche, horizon, niveau, now)

# 🔄 Fallback automatique OpenAI ou Gemini
def analyser_contexte_fallback(marche="forex", horizon="1j", niveau="professionnel", horodatage=None):
    horodatage = horodatage or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    prompt = f"""
Tu es un expert en stratégie de marché comme Warren Buffett et George Soros. Analyse le marché {marche.upper()} à horizon {horizon} pour un niveau {niveau}.
Donne-moi une prédiction, une tendance probable, et une recommandation stratégique concrète.
Réponds en JSON structuré avec : "horodatage", "source", "marche", "horizon", "niveau", "conclusion", "recommandation", "prediction"
"""

    if FALLBACK_MODE == "openai":
        return fallback_openai(prompt, horodatage)
    elif FALLBACK_MODE == "gemini":
        return fallback_gemini(prompt, horodatage)
    else:
        return {
            "horodatage": horodatage,
            "source": "fallback_indisponible",
            "erreur": f"⚠️ Mode de fallback non reconnu : {FALLBACK_MODE}"
        }

# 🧠 Fallback OpenAI (ChatGPT)
def fallback_openai(prompt, horodatage):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un analyste financier stratégique."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        text = response['choices'][0]['message']['content']
        data = json.loads(text)
        data["source"] = "openai"
        data["horodatage"] = horodatage
        return data

    except Exception as e:
        print(f"[❌ GPT] Erreur : {e}")
        return {
            "horodatage": horodatage,
            "source": "openai",
            "erreur": str(e)
        }

# 🧠 Fallback Gemini (Google AI)
def fallback_gemini(prompt, horodatage):
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }

        response = requests.post(
            url=f"{url}?key={GEMINI_API_KEY}",
            headers=headers,
            json=payload
        )

        text = response.json()['candidates'][0]['content']['parts'][0]['text']
        data = json.loads(text)
        data["source"] = "gemini"
        data["horodatage"] = horodatage
        return data

    except Exception as e:
        print(f"[❌ Gemini] Erreur : {e}")
        return {
            "horodatage": horodatage,
            "source": "gemini",
            "erreur": str(e)
        }

# 🧪 Test direct
if __name__ == "__main__":
    print(json.dumps(analyser_contexte("forex", "1j", "professionnel"), indent=2, ensure_ascii=False))
