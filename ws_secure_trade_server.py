import asyncio
import websockets
import json

connected_clients = set()

async def handler(websocket):
    print("🔌 Client connecté")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"📩 Message reçu : {message}")
            data = json.loads(message)

            if data.get("type") == "SIGNAL_FROM_POPUP":
                # TODO : Traiter le signal, sauvegarder, journaliser, déclencher exécution réelle…
                print("✅ Signal validé manuellement :", data.get("payload"))
                await websocket.send(json.dumps({"status": "received", "code": 200}))

    except websockets.exceptions.ConnectionClosed:
        print("❌ Client déconnecté")
    finally:
        connected_clients.remove(websocket)

async def main():
    print("🔐 Lancement du serveur WebSocket sécurisé sur ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # Ne termine jamais (server infini)

if __name__ == "__main__":
    asyncio.run(main())
