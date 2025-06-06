# 2_Trading_Auto.py – Interface de trading automatique avec exécution du bot technique

import os
import time
import logging
import streamlit as st
import pandas as pd
from datetime import datetime

from config_state import sidebar_config
from runtime_config import get_runtime_config
from core.core_bot import run_bot
from core.risk_manager import TradeManager
from core.trading_MTX import cloturer_ordre

# ----------------- Initialisation -----------------
CONFIG = get_runtime_config()
symbol = CONFIG.get("symbol", "EURUSD=X")
use_ai = CONFIG.get("use_ai", False)
capital = CONFIG.get("capital", 1000)
interval = CONFIG.get("interval", 60)

# Gestionnaire de trades
trade_manager = TradeManager(capital=capital)

# Configuration des logs
log_file = f"logs/trading_auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------- Affichage initial -----------------
print("🔁 Lancement du bot de trading automatique...")
print(f"✅ Actif : {symbol} | IA activée : {use_ai} | Intervalle : {interval}s")
logging.info("Démarrage du bot automatique avec IA : %s | Capital initial : %s", use_ai, capital)

# ----------------- Boucle principale -----------------
try:
    losses = 0
    gains = 0

    while True:
        decision, result = run_bot(symbol, use_ai, trade_manager)

        if result == "gain":
            gains += 1
            losses = 0
        elif result == "perte":
            losses += 1
        else:
            logging.warning("Résultat inconnu du trade : %s", result)

        logging.info("Résultat du trade : %s | Total gains : %d | Total pertes : %d", result, gains, losses)

        # 📉 Arrêt conditionnel si 3 pertes consécutives
        if losses >= 3:
            logging.warning("⛔ Bot arrêté après 3 pertes consécutives.")
            print("⚠️ Bot arrêté : 3 pertes consécutives.")
            break

        # 💰 Vérification capital minimal
        if trade_manager.capital < 10:
            logging.warning("⛔ Bot arrêté : capital trop bas.")
            print("⚠️ Bot arrêté : capital insuffisant.")
            break

        time.sleep(interval)

except KeyboardInterrupt:
    print("⛔ Bot interrompu manuellement.")
    logging.info("Bot interrompu manuellement par l'utilisateur.")
