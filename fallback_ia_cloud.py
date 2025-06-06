import os
import openai
import requests

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join("THED", ".env"))

# 🔑 Récupération des clés et priorité IA
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
PREFERED = os.getenv("PREFERED_AI_FALLBACK", "openai").lower()

def fallback_ia_cloud(prompt):
    if PREFERED == "openai" and OPENAI_API_KEY:
        return call_openai(prompt)
    elif PREFERED == "gemini" and GEMINI_API_KEY:
        return call_gemini(prompt)
    elif PREFERED == "mistral" and MISTRAL_API_KEY:
        return call_mistral(prompt)
    elif PREFERED == "groq" and GROQ_API_KEY:
        return call_groq(prompt)
    elif PREFERED == "openrouter" and OPENROUTER_API_KEY:
        return call_openrouter(prompt)
    else:
        return {"error": f"Aucune IA cloud disponible pour fallback : {PREFERED}"}

# 🌩️ Implémentation OpenAI
def call_openai(prompt):
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# 🌩️ Gemini
def call_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    res = requests.post(url, json=body)
    return res.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Erreur")

# 🌩️ Mistral
def call_mistral(prompt):
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    json_data = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=json_data)
    return res.json()["choices"][0]["message"]["content"]

# 🌩️ Groq
def call_groq(prompt):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    json_data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=json_data)
    return res.json()["choices"][0]["message"]["content"]

# 🌩️ OpenRouter
def call_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://thed-bot.com",  # facultatif
        "X-Title": "TIB_BOT_Fallback"
    }
    json_data = {
        "model": "openrouter/mistral-7b",
        "messages": [{"role": "user", "content": prompt}]
    }
    res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=json_data)
    return res.json()["choices"][0]["message"]["content"]
