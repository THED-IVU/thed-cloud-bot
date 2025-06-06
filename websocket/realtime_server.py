import asyncio
import websockets
import json
import datetime
from core.firebase_sync import push_trade_to_firebase  # 🔗 Synchro Firebase automatique

async def handler(websocket, path):
    async for message in websocket:
        try:
            data = json.loads(message)

            # Journalisation locale dans le CSV
            with open("trade_logs/ws_signals_log.csv", "a", encoding="utf-8") as f:
                log_line = (
                    f"{datetime.datetime.now().isoformat()},"
                    f"{data.get('symbol')},{data.get('direction')},"
                    f"{data.get('score')},{data.get('contexte')},"
                    f"{data.get('mise')},{data.get('duree')},"
                    f"{data.get('resume_technique')},{data.get('resume_fondamentale')}\n"
                )
                f.write(log_line)

            # 🔄 Synchronisation automatique dans Firebase
            trade_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "symbol": data.get("symbol"),
                "direction": data.get("direction"),
                "score": data.get("score"),
                "contexte": data.get("contexte"),
                "mise": data.get("mise"),
                "duree": data.get("duree"),
                "resume_technique": data.get("resume_technique"),
                "resume_fondamentale": data.get("resume_fondamentale"),
                "source": "WebSocket"
            }
            push_trade_to_firebase(trade_data)

            print(f"✅ Trade reçu, journalisé et envoyé à Firebase : {data}")

        except Exception as e:
            print(f"❌ Erreur dans le traitement du signal : {e}")

start_server = websockets.serve(handler, "localhost", 8765)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_server)
    print("📡 Serveur WebSocket en écoute sur ws://localhost:8765")
    asyncio.get_event_loop().run_forever()
