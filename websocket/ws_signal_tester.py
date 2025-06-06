
import json
import asyncio
import websockets

# Remplacer par ton WebSocket distant (Render) si activé
WS_URL = "ws://localhost:8765"  # ou "wss://tib-ws-ia.onrender.com"

async def envoyer_signal():
    signal = {
        "symbol": "EURUSD",
        "direction": "achat",
        "score": 88,
        "contexte": "Retournement haussier",
        "resume": "EMA croisé + RSI au-dessus de 50",
        "fondamental": "Pas de nouvelle majeure",
        "mise": "5",
        "duree": "60"
    }
    message = json.dumps(signal)
    try:
        async with websockets.connect(WS_URL) as ws:
            await ws.send(message)
            print("✅ Signal envoyé :", message)
    except Exception as e:
        print("❌ Erreur lors de l’envoi :", e)

if __name__ == "__main__":
    asyncio.run(envoyer_signal())
