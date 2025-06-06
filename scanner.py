# --- scanner.py ---
import os
import time
import pandas as pd
from datetime import datetime
from indicators import calculer_tous_les_indicateurs, signal_strength
from runtime_config import get_runtime_config

try:
    import MetaTrader5 as mt5
    MT5_OK = mt5.initialize()
except:
    MT5_OK = False

import yfinance as yf  # À installer si manquant

LISTE_ACTIFS_YF = [
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "AUDUSD=X", "USDCAD=X",
    "BTC-USD", "ETH-USD"
]

# ✅ Fonction réutilisable
def get_active_assets(source="auto"):
    actifs = []

    if source == "mt5" or (source == "auto" and MT5_OK):
        if not mt5.initialize():
            print("❌ Connexion MT5 échouée")
            return LISTE_ACTIFS_YF

        try:
            symbols = mt5.symbols_get()
            visibles = [s.name for s in symbols if s.visible and "USD" in s.name]
            for sym in visibles:
                tick = mt5.symbol_info_tick(sym)
                if tick and tick.ask > 0 and tick.bid > 0:
                    actifs.append(sym)
                time.sleep(0.05)
        finally:
            mt5.shutdown()

    elif source == "hybrid":
        actifs = LISTE_ACTIFS_YF.copy()
        if MT5_OK:
            try:
                if not mt5.initialize():
                    print("❌ MT5: init échoué")
                    return actifs
                symbols = mt5.symbols_get()
                for s in symbols:
                    if s.visible and "USD" in s.name:
                        tick = mt5.symbol_info_tick(s.name)
                        if tick and tick.ask > 0 and tick.bid > 0:
                            actifs.append(s.name)
                actifs = list(set(actifs))  # supprimer doublons
            finally:
                mt5.shutdown()
    else:
        actifs = LISTE_ACTIFS_YF

    print(f"✅ {len(actifs)} actifs détectés ({source})")
    return actifs
