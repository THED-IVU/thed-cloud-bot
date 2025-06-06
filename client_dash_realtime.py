import asyncio
import websockets

async def lire_signaux():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()
            print(f"📡 Signal reçu : {data}")

asyncio.run(lire_signaux())
