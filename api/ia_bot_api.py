# 📄 Fichier : api/ia_bot_api.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from core.risk_manager import trade_manager  # instance du gestionnaire
from core.trading_MTX import cloturer_ordre

try:
    import MetaTrader5 as mt5
    MT5_OK = mt5.initialize()
except:
    MT5_OK = False

app = Flask(__name__)
CORS(app)  # Autorise les appels CORS (frontend ou autre outil)

@app.route("/")
def index():
    return {"status": "OK", "message": "API Bot IA opérationnelle"}

@app.route("/get_stats", methods=["GET"])
def get_stats():
    return jsonify(trade_manager.get_stats())

@app.route("/set_risk_config", methods=["POST"])
def set_risk_config():
    data = request.json
    if not isinstance(data, dict):
        return jsonify({"error": "Format JSON attendu"}), 400
    trade_manager.update_config(data)
    return jsonify({"status": "success", "new_config": trade_manager.get_stats()})

@app.route("/run_test_strategy", methods=["POST"])
def run_test_strategy():
    data = request.json or {}
    actif = data.get("symbol", "EURUSD=X")
    rsi = data.get("rsi", 25)
    macd = data.get("macd", 0.01)
    macds = data.get("macds", -0.01)

    if rsi < 30 and macd > macds:
        decision = "BUY"
        score = 85
    elif rsi > 70 and macd < macds:
        decision = "SELL"
        score = 82
    else:
        decision = "HOLD"
        score = 60

    return {
        "symbol": actif,
        "RSI": rsi,
        "MACD": macd,
        "MACDs": macds,
        "decision": decision,
        "score": score,
        "timestamp": datetime.now().isoformat()
    }

@app.route("/close_trade", methods=["POST"])
def api_close_trade():
    data = request.json or {}
    symbol = data.get("symbol", "EURUSD")
    result = cloturer_ordre(symbol)
    return jsonify(result)

@app.route("/close_all", methods=["POST"])
def api_close_all():
    if not MT5_OK:
        return jsonify({"statut": "ko", "message": "MT5 non disponible"})
    positions = mt5.positions_get()
    if not positions:
        return jsonify({"statut": "ok", "message": "Aucune position ouverte"})
    clotures = []
    for pos in positions:
        res = cloturer_ordre(pos.symbol)
        clotures.append({"symbol": pos.symbol, **res})
    return jsonify({"statut": "ok", "resultats": clotures})

@app.route("/open_positions", methods=["GET"])
def api_open_positions():
    if not MT5_OK:
        return jsonify({"statut": "ko", "message": "MT5 non disponible"})
    positions = mt5.positions_get()
    if not positions:
        return jsonify({"statut": "ok", "positions": []})
    infos = []
    for p in positions:
        infos.append({
            "symbol": p.symbol,
            "volume": p.volume,
            "price_open": p.price_open,
            "sl": p.sl,
            "tp": p.tp,
            "profit": p.profit
        })
    return jsonify({"statut": "ok", "positions": infos})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
