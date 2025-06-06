import datetime
import os
import json
import random

# Simulation d’une base d’ordres ouverts (à remplacer par un vrai système de suivi réel)
ORDRES_OUVERTS_PATH = "logs/ordres_ouverts.json"
CLOTURES_LOG_PATH = "logs/forex_closures.log"

def charger_ordres_ouverts():
    if os.path.exists(ORDRES_OUVERTS_PATH):
        with open(ORDRES_OUVERTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def enregistrer_ordres_ouverts(ordres):
    with open(ORDRES_OUVERTS_PATH, "w", encoding="utf-8") as f:
        json.dump(ordres, f, indent=2)

def cloturer_trade_forex(symbol):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{now}] ⚠️ Trade Forex clôturé manuellement pour l’actif : {symbol}"
    try:
        with open(CLOTURES_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")
        return log_message
    except Exception as e:
        return f"Erreur lors de la clôture : {e}"

def cloture_auto_si_tp_sl(symbol, prix_actuel):
    ordres = charger_ordres_ouverts()
    ordres_restants = []
    clotures = []

    for ordre in ordres:
        if ordre["symbol"] != symbol:
            ordres_restants.append(ordre)
            continue

        direction = ordre.get("direction", "buy")
        tp = ordre.get("tp")
        sl = ordre.get("sl")
        open_price = ordre.get("prix_ouverture")

        if direction == "buy":
            if prix_actuel >= tp:
                clotures.append(_log_cloture_auto(ordre, "TP atteint", prix_actuel))
            elif prix_actuel <= sl:
                clotures.append(_log_cloture_auto(ordre, "SL atteint", prix_actuel))
            else:
                ordres_restants.append(ordre)
        elif direction == "sell":
            if prix_actuel <= tp:
                clotures.append(_log_cloture_auto(ordre, "TP atteint", prix_actuel))
            elif prix_actuel >= sl:
                clotures.append(_log_cloture_auto(ordre, "SL atteint", prix_actuel))
            else:
                ordres_restants.append(ordre)

    enregistrer_ordres_ouverts(ordres_restants)
    return clotures

def _log_cloture_auto(ordre, raison, prix_actuel):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = (f"[{now}] ✅ Clôture automatique {raison} | "
           f"{ordre['symbol']} @ {prix_actuel:.5f} | Sens : {ordre['direction']} | TP : {ordre['tp']} | SL : {ordre['sl']}")
    with open(CLOTURES_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    return msg

def ajouter_ordre_ouvert(trade_info):
    ordres = charger_ordres_ouverts()
    nouveau = {
        "symbol": trade_info["symbol"],
        "direction": trade_info["direction"],
        "tp": trade_info.get("tp", 0.0),
        "sl": trade_info.get("sl", 0.0),
        "prix_ouverture": simuler_prix_ouverture(),  # À remplacer par le prix réel via MT5
        "datetime": trade_info["datetime"],
        "window": trade_info["window"]
    }
    ordres.append(nouveau)
    enregistrer_ordres_ouverts(ordres)

def simuler_prix_ouverture():
    return round(1.1000 + random.uniform(-0.005, 0.005), 5)  # Simule un prix
