# backtest.py

import os
import argparse
import pandas as pd
import yfinance as yf
from datetime import datetime

from indicators import calculer_tous_les_indicateurs
from ai import analyser_avec_ia
from runtime_config import get_runtime_config  # 🔄 Plus de circular import
from scanner import get_active_assets

# ----------- ARGUMENTS CLI (ligne de commande) -----------
parser = argparse.ArgumentParser(description="Backtest IA + stratégie technique")
parser.add_argument("--symbols", nargs="+", default=[], help="Liste d'actifs à tester (laisse vide pour scan automatique)")
parser.add_argument("--interval", default="15m", help="Intervalle de données (ex: 1m, 5m, 15m, 1h, 1d)")
parser.add_argument("--period", default="1mo", help="Période à analyser (ex: 1d, 5d, 1mo, 6mo)")
parser.add_argument("--balance", type=float, default=1000, help="Solde initial pour le backtest")
parser.add_argument("--no-ai", action="store_true", help="Désactiver totalement l'IA (mode technique seul)")
parser.add_argument("--output-dir", default="exports", help="Dossier de sauvegarde des résultats CSV")
args = parser.parse_args()

# ----------- CONFIG IA DYNAMIQUE -----------
CONFIG = get_runtime_config()
use_ai = CONFIG.get("use_ai", False) and not args.no_ai
api_freq = 3  # Appel IA toutes les 3 bougies

# ----------- STRATÉGIE TECHNIQUE DE BASE -----------
def strategie_technique(row):
    if row["rsi"] < 30 and row["MACD_12_26_9"] > row["MACDs_12_26_9"]:
        return "BUY"
    elif row["rsi"] > 70 and row["MACD_12_26_9"] < row["MACDs_12_26_9"]:
        return "SELL"
    else:
        return "HOLD"

# ----------- CRÉATION DU DOSSIER D'EXPORT -----------
os.makedirs(args.output_dir, exist_ok=True)
résumé_global = []

# ----------- DÉTECTION DES ACTIFS -----------
assets = args.symbols if args.symbols else get_active_assets("auto")

# ----------- LANCEMENT DU BACKTEST MULTI-ACTIF -----------
for symbol in assets:
    print(f"\n📥 Chargement de {symbol} ({args.period} / {args.interval}) ...")
    try:
        data = yf.download(symbol, period=args.period, interval=args.interval).dropna()
        data.columns = [col.lower() for col in data.columns]

        print("⚙️ Calcul des indicateurs ...")
        data = calculer_tous_les_indicateurs(data)

        print("▶ Lancement du backtest ...")
        solde = args.balance
        historique_trades = []

        for i in range(1, len(data)):
            row = data.iloc[i]
            prev = data.iloc[i - 1]
            tech_signal = strategie_technique(row)

            if use_ai:
                if i % api_freq == 0:
                    ia_decision = analyser_avec_ia(data.iloc[i-5:i])
                ia_signal = ia_decision.get("ACTION", "HOLD") if 'ia_decision' in locals() else "HOLD"
            else:
                ia_signal = tech_signal
                ia_decision = {"SCORE": "N/A", "CONTEXT": "TechOnly"}

            if tech_signal == ia_signal and ia_signal in ["BUY", "SELL"]:
                entry = row["close"]
                exit_ = prev["close"]
                profit = (exit_ - entry) if ia_signal == "BUY" else (entry - exit_)

                historique_trades.append({
                    "datetime": row.name,
                    "action": ia_signal,
                    "entry_price": entry,
                    "exit_price": exit_,
                    "profit": profit,
                    "rsi": row["rsi"],
                    "macd": row["MACD_12_26_9"],
                    "macds": row["MACDs_12_26_9"],
                    "ia_score": ia_decision.get("SCORE", "N/A"),
                    "ia_context": ia_decision.get("CONTEXT", "N/A")
                })
                solde += profit

        df_results = pd.DataFrame(historique_trades)

        # ----------- RÉSULTATS DU BACKTEST -----------
        print(f"📊 Résultats du backtest pour {symbol}")
        if df_results.empty:
            print("⚠️ Aucun trade effectué.")
        else:
            print(df_results.tail(5))
            nb = len(df_results)
            gain_moyen = df_results["profit"].mean()
            taux_reussite = (df_results["profit"] > 0).mean() * 100
            solde_final = round(solde, 2)

            print("💼 Solde final :", solde_final)
            print("📈 Nb de trades :", nb)
            print("💰 Gain moyen :", round(gain_moyen, 5))
            print("✅ Taux de réussite :", round(taux_reussite, 2), "%")

            résumé_global.append({
                "Actif": symbol,
                "Solde final": solde_final,
                "Nb trades": nb,
                "Gain moyen": round(gain_moyen, 5),
                "Taux réussite (%)": round(taux_reussite, 2)
            })

            filename = f"{args.output_dir}/backtest_{symbol.replace('=', '').replace('-', '')}.csv"
            df_results.to_csv(filename, index=False)
            print(f"💾 Résultats sauvegardés dans {filename}")

    except Exception as e:
        print(f"❌ Erreur sur {symbol} :", e)

# ----------- RÉCAPITULATIF GLOBAL -----------
if résumé_global:
    df_global = pd.DataFrame(résumé_global)
    print("\n🧾 Récapitulatif multi-actifs :")
    print(df_global.to_string(index=False))

    df_global.to_csv(f"{args.output_dir}/resume_global.csv", index=False)
    print(f"📦 Résumé global exporté dans {args.output_dir}/resume_global.csv")
