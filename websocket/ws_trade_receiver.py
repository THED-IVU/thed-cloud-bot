# ws_trade_receiver.py – Récepteur WebSocket pour signaux IA TIB

import asyncio
import websockets
import json
import logging
from datetime import datetime
import os

# === IMPORT DE LA FONCTION D’EXÉCUTION RÉELLE ===
from pocket_executor import executer_trade_binaires  # ou from mt5_executor import executer_trade_mt5

# === CONFIGURATION ===
AUTO_EXECUTION = True  # ✅ Lance une action dès réception
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "received_trades.log")
WEBSOCKET_PORT = 8777

# === CRÉATION DOSSIER LOGS SI NÉCESSAIRE ===
os.makedirs(LOG_DIR, exist_ok=True)

# === LOGGING GLOBAL ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "receiver_activity.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ws_trade_receiver")

# === TRAITEMENT DU SIGNAL REÇU ===
def traiter_signal(signal):
    logger.info(f"📥 Signal reçu : {signal}")

    if AUTO_EXECUTION:
        try:
            resultat = executer_trade_binaires(signal)  # ou executer_trade_mt5(signal)
            logger.info(f"📤 Exécution réelle : {resultat}")
        except Exception as e:
            logger.error(f"❌ Erreur lors de l’exécution réelle : {e}")
    else:
        print(f"🚀 [SIMU] {signal.get('direction', 'N/A')} sur {signal.get('symbol', '??')} "
              f"({signal.get('mise', '?')}$ / {signal.get('duree', '?')}s)")

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(signal) + "\n")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l’écriture dans le fichier log : {e}")

# === GESTIONNAIRE WS POUR CHAQUE CLIENT ===
async def handler(websocket):  # ✅ Correction : 1 seul paramètre
    logger.info("🟢 Nouveau client connecté.")
    try:
        async for message in websocket:
            try:
                signal = json.loads(message)
                traiter_signal(signal)
                await websocket.send("✅ Signal reçu et traité.")
            except json.JSONDecodeError:
                logger.error(f"❌ Erreur JSON : {message}")
                await websocket.send("❌ Erreur JSON dans le message reçu.")
    except websockets.exceptions.ConnectionClosedOK:
        logger.info("🔌 Client déconnecté proprement.")
    except Exception as e:
        logger.error(f"⚠️ Erreur WebSocket : {e}")

# === LANCEMENT DU SERVEUR WS ===
async def main():
    logger.info(f"🚀 Serveur WebSocket démarré sur ws://localhost:{WEBSOCKET_PORT}")
    async with websockets.serve(handler, "localhost", WEBSOCKET_PORT):
        await asyncio.Future()  # serveur tourne à l'infini

if __name__ == "__main__":
    asyncio.run(main())
