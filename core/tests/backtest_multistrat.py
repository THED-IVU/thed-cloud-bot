# 📄 Fichier : backtest.py

import pandas as pd
from datetime import datetime
from core.core_bot import STRATEGIES
from core.risk_manager import TradeManager
from core.strategie_ema_rsi import detecter_opportunite as strategie_ema_rsi
from core.strategie_breakout_news import detecter_opportunite as strategie_breakout_news
from core.strategie_heikin_psar import detecter_opportunite as strategie_heikin_psar
from core.strategie_fibo_bougies import detecter_opportunite as strategie_fibo_bougies
from core.strategie_sniper_ia import detecter_opportunite as strategie_sniper_ia
from scanner import LISTE_ACTIFS

# Simule une session complète sans connexion MT5 (mode dry-run)
def backtest_strategies(capital=1000, score_min=70):
    historique = []
    manager = TradeManager(capital=capital)

    for symbole in LISTE_ACTIFS:
        for priority, nom_strategie, strategie in sorted(STRATEGIES):
            try:
                res = strategie(symbole)
                if res and res['score'] >= score_min:
                    resultat_trade = {
                        "datetime": datetime.now().isoformat(),
                        "symbol": symbole,
                        "strat": nom_strategie,
                        "decision": res["decision"],
                        "score": res["score"],
                        "sl": res["sl"],
                        "tp": res["tp"],
                        "profit": 10 if res["decision"] != "HOLD" else 0,
                        "capital": round(manager.capital, 2)
                    }
                    if resultat_trade["profit"] > 0:
                        manager.capital += resultat_trade["profit"]
                    historique.append(resultat_trade)
                    break  # on arrête dès qu'une stratégie valide est trouvée
            except Exception as e:
                print(f"Erreur {nom_strategie} sur {symbole} : {e}")

    return pd.DataFrame(historique)

if __name__ == "__main__":
    df = backtest_strategies()
    print(df)
    df.to_csv("backtest_resultats.csv", index=False)
