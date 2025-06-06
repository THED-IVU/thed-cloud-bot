# core/trading_mt5.py

import MetaTrader5 as mt5
from datetime import datetime
import time

# Connexion à MT5
if not mt5.initialize():
    raise RuntimeError(f"❌ Échec d'initialisation de MT5 : {mt5.last_error()}")

def fermer_connexion():
    mt5.shutdown()

def convertir_direction(decision):
    return mt5.ORDER_TYPE_BUY if decision.lower() == "buy" else mt5.ORDER_TYPE_SELL

def executer_trade(symbol, decision, lot, sl, tp, magic=1001):
    """
    Envoie un ordre au marché avec stop-loss et take-profit.
    Retourne le statut et un résultat simplifié.
    """
    try:
        # Récupération des infos de marché
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            raise ValueError(f"Symbole introuvable : {symbol}")

        if not symbol_info.visible:
            mt5.symbol_select(symbol, True)

        prix = mt5.symbol_info_tick(symbol).ask if decision == "buy" else mt5.symbol_info_tick(symbol).bid
        deviation = 10

        # Création de la requête
        ordre = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": convertir_direction(decision),
            "price": prix,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": magic,
            "comment": "Bot IA v1",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(ordre)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"❌ Erreur ordre : {result.retcode}")
            return {
                "statut": "erreur",
                "retcode": result.retcode,
                "profit": 0,
                "prix_ouverture": prix
            }

        print(f"✅ Trade exécuté : {decision.upper()} {symbol} | Prix : {prix} | Lot : {lot}")
        return {
            "statut": "ok",
            "ticket": result.order,
            "profit": 0,  # Le profit réel sera calculé à la clôture
            "prix_ouverture": prix
        }

    except Exception as e:
        print(f"❌ Exception lors du trade : {e}")
        return {
            "statut": "exception",
            "retcode": -1,
            "profit": 0,
            "prix_ouverture": 0
        }
