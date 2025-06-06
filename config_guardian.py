# 📄 config_guardian.py – Paramètres de configuration du Guardian IA

# Liste des modules critiques à surveiller
MODULES_CLES = [
    "core.core_bot",
    "core.trading_MTX",
    "core.learning_tracker",
    "core.risk_manager",
    "core.news_fetcher",
    "ai",
    "main_launcher"
]

# Délai de réflexion avant exécution automatique (en secondes)
DELAI_AUTORISATION_UTILISATEUR = 10

# API externes utilisées (pour suivi quotas ou mises à jour)
API_CONFIG = {
    "openai": {
        "key_env": "OPENAI_API_KEY",
        "payant": True
    },
    "gemini": {
        "key_env": "GEMINI_API_KEY",
        "payant": False
    }
}

# Endpoints de synchronisation cloud
CLOUD_SYNC = {
    "firebase_logs": "https://your-firebase-endpoint.example.com/sync",
    "backup_logs": "https://your-other-backup-endpoint.com"
}

# Informations version/abonnement (pour monitoring)
SOFTWARE_VERSION = {
    "type": "free",  # valeurs possibles : "free", "trial", "premium"
    "exp_date": None,
    "restrictions": ["nombre appels API", "multi-fenêtres limité"]
}

# Activation des popups console robot (True/False)
AFFICHER_POPUPS_CONSOLE = True
