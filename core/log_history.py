
import pandas as pd
from datetime import datetime
import os

def ajouter_log_execution(trade, fichier="trade_logs/historique_trades.csv"):
    os.makedirs("trade_logs", exist_ok=True)
    df = pd.DataFrame([{
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symbol": trade["symbol"],
        "direction": trade["direction"],
        "mise": trade["mise"],
        "duree": trade["duree"],
        "confiance": trade.get("confiance", "N/A"),
        "validation": trade.get("validation", "manuelle")
    }])
    if os.path.exists(fichier):
        df.to_csv(fichier, mode='a', header=False, index=False)
    else:
        df.to_csv(fichier, index=False)
