import asyncio
import websockets
import json
from datetime import datetime

clients = set()

async def notifier_clients():
    while True:
        if clients:
            message = json.dumps({
                "symbol": "BTCUSD",
                "timestamp": datetime.now().isoformat(),
                "direction": "BUY",
                "confiance": "7.5/10"
            })
            await asyncio.wait([client.send(message) for client in clients])
        await asyncio.sleep(5)

async def handler(websocket, path):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

start_server = websockets.serve(handler, "localhost", 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)
loop.create_task(notifier_clients())
loop.run_forever()
