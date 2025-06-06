
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import websocket
import json
import threading

app = dash.Dash(__name__)
app.title = "Client Dash - Signaux Temps Réel"

signal_data = {"symbol": "", "direction": "", "score": "", "timestamp": ""}

app.layout = html.Div([
    html.H1("📡 Lecture en temps réel des signaux IA", style={"textAlign": "center"}),
    html.Div(id="signal-output", style={"fontSize": 22, "textAlign": "center", "marginTop": "20px"}),
    dcc.Interval(id="interval", interval=2000, n_intervals=0)
])

@app.callback(
    Output("signal-output", "children"),
    Input("interval", "n_intervals")
)
def update_signal(n):
    return f"⏱️ {signal_data['timestamp']} | 📈 {signal_data['symbol']} | 📊 {signal_data['direction']} | 🔢 Score : {signal_data['score']}"

def on_message(ws, message):
    global signal_data
    try:
        data = json.loads(message)
        signal_data.update(data)
    except Exception as e:
        print("Erreur de parsing :", e)

def on_error(ws, error):
    print("Erreur WebSocket :", error)

def on_close(ws, close_status_code, close_msg):
    print("Connexion WebSocket fermée.")

def on_open(ws):
    print("Connexion WebSocket ouverte.")

def run_ws():
    ws = websocket.WebSocketApp("ws://localhost:8765", on_open=on_open,
                                on_message=on_message, on_error=on_error, on_close=on_close)
    ws.run_forever()

thread = threading.Thread(target=run_ws)
thread.daemon = True
thread.start()

if __name__ == "__main__":
    app.run_server(debug=True)
