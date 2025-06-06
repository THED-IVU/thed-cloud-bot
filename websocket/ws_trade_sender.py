
# ws_trade_sender.py – Simulation IA + Envoi hybride (WebSocket / Flask / Exécution Réelle)
import asyncio
import websockets
import websocket
import requests
import json
import random
import time
import threading
import logging
from datetime import datetime

# === CONFIGURATIONS GLOBALES ===
USE_REAL_EXECUTION = True       # ✅ Activer exécution réelle
MODE_TRADING = "binaire"        # "binaire" ou "forex"
MODE = "WS_LOCAL"  # <-- Utilise le WebSocket local, qui fonctionne déjà
FLASK_API_URL = "http://127.0.0.1:8000/send_trade"
POCKET_OPTION_WS_URL = "wss://ws.pocketoption.com/demo"
LOCAL_SIMULATION_URL = "ws://localhost:8777"

logger = logging.getLogger("ws_trade_sender")
logging.basicConfig(level=logging.INFO)

# === GÉNÉRATEUR DE SIGNAUX ===
def generate_fake_trade():
    return {
        "timestamp": datetime.now().isoformat(),
        "symbol": random.choice(["EURUSD", "BTCUSD", "ETHUSD", "USDJPY"]),
        "direction": random.choice(["up", "down"]),
        "score": round(random.uniform(60, 95), 2),
        "contexte": random.choice(["Range", "Expansion", "Retournement"]),
        "mise": random.randint(10, 100),
        "duree": 30 if MODE_TRADING == "binaire" else 120,
        "resume_technique": "RSI=72.5, EMA9>EMA21, MACD haussier",
        "resume_fondamentale": "Pas de news critique"
    }

# === FORMAT POUR WEBSOCKET PO ===
def build_trade_message(data):
    return {
        "action": "trade",
        "params": {
            "symbol": data.get("symbol", "EURUSD"),
            "direction": data.get("direction", "up"),
            "amount": data.get("mise", 1),
            "duration": data.get("duree", 30),
            "timestamp": int(time.time())
        }
    }

# === ENVOI VERS POCKET OPTION (RÉEL via WebSocket) ===
def envoyer_ordre_pocket_option(data: dict):
    try:
        ws = websocket.WebSocket()
        logger.info(f"🔌 Connexion WebSocket à {POCKET_OPTION_WS_URL}…")
        ws.connect(POCKET_OPTION_WS_URL)
        message = json.dumps(build_trade_message(data))
        logger.info(f"📤 Envoi de l’ordre : {message}")
        ws.send(message)
        response = ws.recv()
        logger.info(f"📥 Réponse Pocket Option : {response}")
        ws.close()
        return True, response
    except Exception as e:
        logger.error(f"❌ Erreur WebSocket PO : {e}")
        return False, str(e)

def envoyer_ordre_async(data: dict):
    thread = threading.Thread(target=envoyer_ordre_pocket_option, args=(data,))
    thread.start()

# === ALGORITHME UNIFIÉ D’ENVOI DE SIGNAUX ===
def envoyer_signal(signal):
    if USE_REAL_EXECUTION:
        if MODE_TRADING == "binaire":
            executer_binaire(signal)
        elif MODE_TRADING == "forex":
            executer_forex(signal)
    else:
        print("📩 [SIMULATION] Signal :", signal)

def executer_binaire(signal):
    try:
        print("🟦 Envoi vers Pocket Option - Mode Binaire")
        print(f"✅ Simulation: Direction {signal['direction']} sur {signal['symbol']}")
    except Exception as e:
        print("❌ Erreur exécution binaire :", e)

def executer_forex(signal):
    try:
        print("🟧 Envoi vers Forex (MT5 WebTerminal ou API)")
        print(f"✅ Simulation forex {signal['symbol']} avec SL/TP à configurer")
    except Exception as e:
        print("❌ Erreur exécution forex :", e)

# === ENVOI FLASK
def send_to_flask_api():
    print("📡 Envoi vers API Flask locale…")
    while True:
        trade = generate_fake_trade()
        try:
            response = requests.post(FLASK_API_URL, json=trade)
            print(f"📤 Signal envoyé à Flask : {trade} | Réponse: {response.status_code}")
            envoyer_signal(trade)
        except Exception as e:
            print(f"❌ Erreur API Flask : {e}")
        time.sleep(5)

# === SIMULATION WEBSOCKET LOCAL
async def send_fake_trades_ws(uri):
    print("🧪 Mode simulation WebSocket local activé.")
    while True:
        trade = generate_fake_trade()
        async with websockets.connect(uri) as ws:
            await ws.send(json.dumps(trade))
            print(f"📤 Signal simulé envoyé : {trade}")
        time.sleep(5)

# === TEST INDÉPENDANT : Exemple d’envoi unique IA
async def envoyer_signal_exemple(uri="ws://localhost:8777"):
    async with websockets.connect(uri) as websocket:
        signal = {
            "actif": "EURUSD",
            "direction": random.choice(["HAUT", "BAS"]),
            "mise": 1.5,
            "duree": 60,
            "origine": "IA_TIB_Guardian",
            "timestamp": time.time()
        }
        await websocket.send(json.dumps(signal))
        print(f"✅ Signal IA simulé envoyé : {signal}")

# === MAIN EXECUTION
if __name__ == "__main__":
    print(f"🚀 Démarrage en mode {MODE.upper()} | Trading : {MODE_TRADING} | Réel : {USE_REAL_EXECUTION}")
    if MODE == "WS_LOCAL":
        asyncio.get_event_loop().run_until_complete(send_fake_trades_ws(LOCAL_SIMULATION_URL))
    elif MODE == "WS_REAL":
        exemple = generate_fake_trade()
        envoyer_ordre_async(exemple)
    elif MODE == "FLASK":
        send_to_flask_api()
    else:
        asyncio.run(envoyer_signal_exemple())  # test rapide
