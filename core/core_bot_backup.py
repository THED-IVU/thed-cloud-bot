from datetime import datetime
from core.risk_manager import TradeManager
from core.strategie_ema_rsi import detecter_opportunite as strategie_ema_rsi
from core.strategie_breakout_news import detecter_opportunite as strategie_breakout
from core.strategie_heikin_psar import detecter_opportunite as strategie_heikin
from core.strategie_fibo_bougies import detecter_opportunite as strategie_fibo
from core.strategie_sniper_ia import detecter_opportunite as strategie_sniper
from core.trading_MTX import executer_trade
from scanner import get_active_assets
from db import enregistrer_trade
from runtime_config import get_runtime_config
from core.learning_tracker import get_weights_and_thresholds
from core.firebase_logger import envoyer_log_firebase

config = get_weights_and_thresholds()
poids_ia = config["ia_validation_weight"]
poids_tech = config["technique_weight"]
seuil_global = config["global_score_threshold"]

STRATEGIES = [
    (0, "Sniper IA", strategie_sniper),
    (1, "Breakout + News", strategie_breakout),
    (2, "Heikin Ashi + PSAR", strategie_heikin),
    (3, "Fibonacci + Bougies", strategie_fibo),
    (4, "EMA + RSI + MACD", strategie_ema_rsi)
]

SEUIL_SCORE = 70
RISK_PERCENT = 0.02
trade_manager = TradeManager(capital=1000)

def run_bot():
    CONFIG = get_runtime_config()
    use_ai = CONFIG.get("use_ai", False)
    actifs = get_active_assets("auto")

    for symbole in actifs:
        meilleures_signaux = []

        for priorite, nom_strategie, strategie in sorted(STRATEGIES):
            try:
                resultat = strategie(symbole, use_ai=use_ai)
                if resultat and resultat["score"] >= SEUIL_SCORE:
                    meilleures_signaux.append((priorite, nom_strategie, resultat))
            except Exception as e:
                print(f"❌ Erreur stratégie {nom_strategie} sur {symbole} : {e}")

        if meilleures_signaux and trade_manager.running:
            meilleures_signaux.sort(key=lambda x: x[0])
            priorite, nom_strategie, resultat = meilleures_signaux[0]

            taille_lot = trade_manager.compute_position_size(pip_value=10)
            decision = resultat["decision"]
            sl = resultat["sl"]
            tp = resultat["tp"]

            resultat_trade = executer_trade(symbole, decision, taille_lot, sl, tp)
            trade_manager.on_trade_result(resultat_trade)

            trade_data = {
                "datetime": datetime.now().isoformat(),
                "action": decision,
                "price": resultat_trade.get("prix_ouverture"),
                "exit_price": 0,
                "profit": resultat_trade.get("profit", 0),
                "RSI": resultat.get("rsi", 0),
                "MACD": resultat.get("macd", 0),
                "MACDs": resultat.get("macds", 0),
                "EMA9": resultat.get("ema9", 0),
                "EMA21": resultat.get("ema21", 0),
                "source": nom_strategie,
                "context": resultat.get("context", "-"),
                "note": resultat.get("score", 0),
                "score_ia": resultat.get("score_ia", "-"),
                "validation_ia": resultat.get("validation_ia", "-"),
                "explication_ia": resultat.get("explication_ia", "-"),
                "asset": symbole,
                "capital": round(trade_manager.capital, 2)
            }

            enregistrer_trade(trade_data)
            envoyer_log_firebase(symbole, f"Trade {decision}", resultat_trade.get("profit", 0), nom_strategie)

    print(f"🕒 Exécution terminée à {datetime.now()}")

if __name__ == "__main__":
    run_bot()