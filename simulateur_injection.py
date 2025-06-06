import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "trades.db"

SYMBOLS = ["EURUSD", "BTCUSD", "USDJPY", "ETHUSD"]
MODES = ["binaire", "forex"]
CONTEXTES = ["Range", "Retournement", "Expansion"]
DIRECTIONS = ["up", "down"]

def generer_faux_trade():
    symbol = random.choice(SYMBOLS)
    mode = "binaire" if symbol in ["BTCUSD", "ETHUSD"] else "forex"
    return {
        "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 120))).isoformat(),
        "symbol": symbol,
        "direction": random.choice(DIRECTIONS),
        "score": round(random.uniform(60, 95), 2),
        "contexte": random.choice(CONTEXTES),
        "mise": random.randint(10, 100),
        "duree": random.choice([30, 60, 120, 300]),
        "resume_technique": "RSI=72.5, EMA9>EMA21, MACD haussier",
        "resume_fondamentale": "Pas de news critique",
    }

def injecter_faux_trades(nb=50):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for _ in range(nb):
        trade = generer_faux_trade()
        c.execute("""
            INSERT INTO trades (
                timestamp, symbol, direction, score, contexte,
                mise, duree, resume_technique, resume_fondamentale
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            trade["timestamp"],
            trade["symbol"],
            trade["direction"],
            trade["score"],
            trade["contexte"],
            trade["mise"],
            trade["duree"],
            trade["resume_technique"],
            trade["resume_fondamentale"]
        ))
    conn.commit()
    conn.close()
    print(f"✅ {nb} faux trades injectés avec succès.")

if __name__ == "__main__":
    injecter_faux_trades(nb=50)
