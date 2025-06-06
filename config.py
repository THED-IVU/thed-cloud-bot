# config.py

# 💰 Paramètres généraux du bot
INITIAL_BALANCE = 10000
USE_CHATGPT = False           # Active/désactive l’IA dans les stratégies
USE_LIVE_DATA = False         # Mode temps réel (vs historique)
LIMIT_API_CALLS = True        # Réduit les appels API (1 sur N bougies)
API_CALL_FREQUENCY = 10       # Si LIMIT_API_CALLS=True, 1 appel toutes les N bougies

# 📈 Paramètres marché
SYMBOL = "EURUSD=X"
PERIOD = "1mo"
INTERVAL = "1m"

# 🔐 API Keys et URLs (remplacées dynamiquement par .env ou autres moyens)
OPENAI_API_KEY = None  # facultatif ici

# 📁 Fichiers utilisés
HISTORICAL_DB = "historique_trades.db"
PARAMS_FILE = "params.json"

# 🧪 Mode test (affiche infos debug)
DEBUG = True
