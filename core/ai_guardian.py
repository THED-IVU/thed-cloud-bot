# 📄 ai_guardian.py – Agent IA Guardian pour BOT_MT5_THED_PRO

import os
import sys
import json
import time
import importlib
import requests
import subprocess
import traceback
from datetime import datetime

# === Ajout dynamique des chemins ===
from utils.path_utils import ajouter_base_et_sous_dossiers
ajouter_base_et_sous_dossiers()

# === Imports stratégiques ===
from MON_API_PRO.ia_strategique import analyser_contexte
from ia_storage import sauvegarder_analyse_locale, sync_to_firebase
from notifications.ia_alerts import envoyer_alerte_ia

# === Logs ===
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "guardian_actions.log")
ERROR_LOG = os.path.join(LOG_DIR, "errors.log")
SIGNAL_LOG = os.path.join(LOG_DIR, "ia_signals.log")

API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY", ""),
    "gemini": os.getenv("GEMINI_API_KEY", "")
}
CLOUD_ENDPOINT = "https://ia-bot-thed.onrender.com"
VERSION_FILE = "config_guardian.py"

os.makedirs(LOG_DIR, exist_ok=True)

def log_action(action, metadata=None):
    entry = {
        "datetime": datetime.now().isoformat(),
        "action": action,
        "metadata": metadata or {}
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
    with open(SIGNAL_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def log_error(context, exception):
    error_info = {
        "datetime": datetime.now().isoformat(),
        "module": "AI_GUARDIAN",
        "context": context,
        "error": str(exception),
        "trace": traceback.format_exc()
    }
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(error_info) + "\n")

def notify_user(message):
    print(f"🤖 [TIB Guardian] {message}")
    log_action("NOTIFY_USER", {"message": message})

def analyze_module(module_name):
    try:
        module = importlib.import_module(module_name)
        notify_user(f"Module '{module_name}' chargé avec succès.")
    except Exception as e:
        notify_user(f"Erreur dans le module '{module_name}': {e}")
        log_error(f"MODULE: {module_name}", e)

def check_api_quota():
    quotas = {
        "openai": "à vérifier via billing API",
        "gemini": "limite journalière à surveiller"
    }
    log_action("API_QUOTA_CHECK", quotas)

def check_versions():
    try:
        with open(VERSION_FILE, "r") as f:
            content = f.read()
        if "free" not in content:
            notify_user("⚠️ Une version logicielle est peut-être devenue payante.")
    except:
        notify_user("❌ Impossible de vérifier la version logicielle.")

def sync_logs_to_cloud():
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = f.read()
        requests.post(CLOUD_ENDPOINT, data={"logs": data})
        notify_user("☁️ Synchronisation cloud réussie.")
    except Exception as e:
        notify_user(f"⚠️ Erreur de sync cloud : {e}")

def propose_updates():
    updates = [
        {"id": "add_news", "text": "Ajouter nouvelle source d'actualité."},
        {"id": "update_strategy", "text": "Recalibrer RSI + EMA."},
        {"id": "adjust_risk", "text": "Activer gestion de risque dynamique."}
    ]
    for update in updates:
        notify_user(f"💡 Suggestion IA : {update['text']}")
        time.sleep(5)

def launch_robot_popup():
    print("""
    🤖 TIB GUARDIAN POPUP
    ╭────────────────────────────╮
    │  Nouvelle action IA proposée │
    ╰────────────────────────────╯
    """)

def watchdog_executor():
    try:
        print("🔁 Surveillance des algorithmes MT5 activée...")
        import core.trading_MTX as trading_module
        if hasattr(trading_module, "verifier_trades"):
            trading_module.verifier_trades()
        log_action("Surveillance des algorithmes activée")
    except Exception as e:
        log_error("Erreur watchdog_executor", e)

def risk_monitor():
    try:
        print("🛡️ Suivi du risque...")
        from core.risk_manager import analyser_risque
        analyser_risque()
        log_action("Suivi du risque effectué")
    except Exception as e:
        log_error("Erreur risk_monitor", e)

def strategy_updater():
    try:
        print("📊 Mise à jour des stratégies...")
        from core.learning_tracker import mise_a_jour_strategie
        mise_a_jour_strategie()
        log_action("Stratégie mise à jour")
    except Exception as e:
        log_error("Erreur strategy_updater", e)

def permission_manager():
    print("🔐 Permission requise pour décisions critiques")
    log_action("Permission requise")

def external_intelligence():
    try:
        print("🌐 Récupération de news externes...")
        from core.news_fetcher import get_latest_news
        infos = get_latest_news("EURUSD")
        log_action(f"Infos externes récupérées", {"news": infos[:100]})
    except Exception as e:
        log_error("Erreur external_intelligence", e)

def smart_diagnostics():
    try:
        print("🧠 Lancement des diagnostics...")
        modules = ["ai", "core.core_bot", "core.trading_MTX"]
        for mod in modules:
            try:
                importlib.reload(importlib.import_module(mod))
                log_action(f"Module {mod} rechargé avec succès")
            except Exception as err:
                log_error(f"Échec rechargement module {mod}", err)
    except Exception as e:
        log_error("Erreur smart_diagnostics", e)

def analyse_strategique_guardian(marche="forex", horizon="1j", niveau="professionnel"):
    print(f"🧠 Guardian IA - Lancement de l’analyse stratégique : {marche}, {horizon}, {niveau}")
    try:
        analyse = analyser_contexte(marche=marche, horizon=horizon, niveau=niveau)
        print("✅ Analyse IA reçue :", analyse)
        sauvegarder_analyse_locale("stratégique", analyse)
        sync_to_firebase("stratégique", analyse)
        envoyer_alerte_ia(analyse)
        log_action("analyse_strategique", analyse)
        return analyse
    except Exception as e:
        print(f"❌ Erreur Guardian IA : {e}")
        log_error("analyse_strategique", e)
        return {"erreur": str(e), "source": "guardian"}

def main():
    notify_user("👁️ TIB Guardian activé.")
    watchdog_executor()
    risk_monitor()
    strategy_updater()
    permission_manager()
    external_intelligence()
    smart_diagnostics()
    analyse_strategique_guardian("forex", "1j", "professionnel")
    check_api_quota()
    check_versions()
    sync_logs_to_cloud()
    propose_updates()
    launch_robot_popup()
    notify_user("✅ TIB Guardian prêt. En attente d'autorisation utilisateur...")

if __name__ == "__main__":
    main()
