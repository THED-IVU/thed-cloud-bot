from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

last_trade_data = None
DB_PATH = "trades.db"

# 🔧 Initialisation de la base de données
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            direction TEXT,
            score REAL,
            contexte TEXT,
            mise INTEGER,
            duree INTEGER,
            type_trade TEXT,
            stop_loss REAL,
            take_profit REAL,
            resume_technique TEXT,
            resume_fondamentale TEXT
        )
    """)
    conn.commit()
    conn.close()

# 💾 Sauvegarde d'un trade dans la base
def enregistrer_trade_sqlite(data):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO trades (
                timestamp, symbol, direction, score, contexte,
                mise, duree, type_trade, stop_loss, take_profit,
                resume_technique, resume_fondamentale
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("timestamp"),
            data.get("symbol"),
            data.get("direction"),
            data.get("score"),
            data.get("contexte"),
            data.get("mise"),
            data.get("duree"),
            data.get("type_trade", "binaire"),  # par défaut binaire
            data.get("stop_loss"),
            data.get("take_profit"),
            data.get("resume_technique"),
            data.get("resume_fondamentale")
        ))
        conn.commit()
        conn.close()
        print("💾 Trade enregistré avec succès.")
    except Exception as e:
        print(f"❌ Erreur enregistrement SQLite : {e}")

# 📤 Réception des signaux de trade
@app.route("/send_trade", methods=["POST"])
def send_trade():
    global last_trade_data
    try:
        data = request.json
        if not data.get("timestamp"):
            data["timestamp"] = datetime.now().isoformat()
        if "type_trade" not in data:
            data["type_trade"] = "binaire"  # Valeur par défaut

        last_trade_data = data
        enregistrer_trade_sqlite(data)

        type_trade = data["type_trade"]
        if type_trade == "binaire":
            print(f"📘 [BINAIRE] Trade reçu : {data}")
        elif type_trade == "forex":
            print(f"📙 [FOREX] Trade reçu : {data}")
        else:
            print(f"📒 [AUTRE] Trade reçu : {data}")

        return jsonify({"status": "ok", "message": "Trade enregistré avec succès"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 🔍 Dernier trade reçu
@app.route("/last_trade", methods=["GET"])
def last_trade():
    if last_trade_data:
        return jsonify({
            "status": "ok",
            "message": f"Dernier trade IA ({last_trade_data.get('type_trade', 'binaire')})",
            "data": last_trade_data,
            "timestamp": datetime.now().isoformat()
        }), 200
    else:
        return jsonify({
            "status": "ok",
            "message": "Aucun trade reçu pour le moment.",
            "data": {},
            "timestamp": datetime.now().isoformat()
        }), 200

# ▶️ Lancement de l’API Flask
if __name__ == "__main__":
    init_db()
    app.run(port=8000)
