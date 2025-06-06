# 📄 tests/backtest_multi_strategies.py

import pandas as pd
from datetime import datetime, timedelta
from core.strategie_ema_rsi import detecter_opportunite as strategie_ema_rsi
from core.strategie_breakout_news import detecter_opportunite as strategie_breakout
from core.strategie_heikin_psar import detecter_opportunite as strategie_heikin
from core.strategie_fibo_bougies import detecter_opportunite as strategie_fibo
from core.strategie_sniper_ia import detecter_opportunite as strategie_sniper
from db import inserer_trade, initialiser_base

# Initialisation base SQLite
initialiser_base()

# Liste des stratégies
STRATEGIES = [
    ("EMA + RSI + MACD", strategie_ema_rsi),
    ("Breakout + News", strategie_breakout),
    ("Heikin Ashi + PSAR", strategie_heikin),
    ("Fibonacci + Bougies", strategie_fibo),
    ("Sniper IA", strategie_sniper)
]

SYMBOL = "EURUSD=X"
INTERVAL = "15m"
USE_AI = False

# ⏱️ Plage temporelle : du 1er au 10 mai 2025 (exemple)
start_date = datetime(2025, 5, 1)
end_date = datetime(2025, 5, 10)

delta = timedelta(days=1)
results = []

print(f"📊 Backtest de {start_date.date()} à {end_date.date()} sur {SYMBOL}")

while start_date <= end_date:
    for name, strat in STRATEGIES:
        try:
            period_str = (start_date + timedelta(days=1)).strftime("%Y-%m-%d")
            result = strat(SYMBOL, interval=INTERVAL, period="2d", use_ai=USE_AI)

            if result:
                now = datetime.now()
                trade = {
                    "datetime": now.isoformat(),
                    "action": result["decision"],
                    "price": result["entry"],
                    "exit_price": result["tp"],
                    "profit": result["tp"] - result["entry"] if result["decision"] == "buy" else result["entry"] - result["tp"],
                    "RSI": result.get("rsi", 0),
                    "MACD": result.get("macd", 0),
                    "MACDs": result.get("macds", 0),
                    "EMA9": result.get("ema9", 0),
                    "EMA21": result.get("ema21", 0),
                    "source": name,
                    "context": result.get("context", "-"),
                    "note": result.get("score", 0),
                    "score_ia": result.get("score_ia", "-"),
                    "validation_ia": result.get("validation_ia", "-"),
                    "explication_ia": result.get("explication_ia", "-"),
                    "asset": SYMBOL,
                    "capital": 1000  # fictif dans ce test
                }
                results.append(trade)
                inserer_trade(trade)  # 🔄 Envoi vers SQLite

        except Exception as e:
            print(f"❌ Erreur {name} - {SYMBOL} ({start_date.date()}) : {e}")
    start_date += delta

# Résumé
df = pd.DataFrame(results)
if not df.empty:
    print("\n✅ Résultats du backtest :\n")
    stats = df.groupby("source").agg(
        total_signaux=("action", "count"),
        gain_total=("profit", "sum"),
        moyenne_score=("note", "mean")
    )
    print(stats)

    df.to_csv("tests/resultats_backtest_multi.csv", index=False)
    print("\n📁 Résultats exportés dans : tests/resultats_backtest_multi.csv")
else:
    print("⚠️ Aucun signal détecté dans la plage de test.")
