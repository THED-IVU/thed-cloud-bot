
import websocket
import json

def on_message(ws, message):
    print(f"📥 Nouveau message reçu : {message}")

def on_error(ws, error):
    print(f"❌ Erreur WebSocket : {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Connexion WebSocket fermée.")

def on_open(ws):
    print("🔗 Connexion WebSocket ouverte.")
    # Exemple d’envoi de signal IA simulé
    trade_info = {
        "symbol": "EURUSD",
        "direction": "UP",
        "score": 87,
        "contexte": "range haussier",
        "resume_technique": "RSI=71, EMA9>EMA21, MACD positif",
        "resume_fondamentale": "Aucune news critique détectée",
        "mise": 5,
        "duree": 60
    }
    ws.send(json.dumps(trade_info))

if __name__ == "__main__":
    ws = websocket.WebSocketApp("ws://localhost:8765",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
