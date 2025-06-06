# app_config.py

# 1. 🔐 Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
import os
load_dotenv()

# 2. 🧠 (optionnel) init visuel via Streamlit
CONFIG = {}  # init_page ne doit pas être ici, sinon circular import

# 3. ✅ Définir la configuration avec les clés lues depuis le .env
CONFIG = {
    "use_ai": True,
    "ai_provider": "groq",  # gemini, openai, claude, etc.

    "gemini": {
        "api_key": os.getenv("GEMINI_API_KEY"),
        "project_id": "882797834647"
    },
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-3.5-turbo"
    },
    "claude": {
        "api_key": os.getenv("CLAUDE_API_KEY", ""),
        "model": "claude-3-sonnet-20240229"
    },
    "mistral": {
        "api_key": os.getenv("MISTRAL_API_KEY"),
        "model": "mistral-small"
    },
    "groq": {
        "api_key": os.getenv("GROQ_API_KEY"),
        "model": "mixtral-8x7b-32768"
    },
    "openrouter": {
        "api_key": os.getenv("OPENROUTER_API_KEY"),
        "model": "mistralai/mistral-7b-instruct"
    },

    "default_score": "0/10",
    "default_action": "HOLD"
}
