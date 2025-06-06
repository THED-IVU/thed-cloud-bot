
import streamlit as st
import os
import json
from datetime import datetime
from core.trading_MTX import executer_trade
from indicators import calculer_tous_les_indicateurs
from ai import analyser_avec_ia
import pandas as pd
import requests

# === CONFIGURATION ===
st.set_page_config(page_title="Exécution IA + Historique + Telegram", layout="wide")
st.title("🤖 Interface Complète d’Exécution IA (Realtime + Log + Telegram)")

FICHIER_TRADES = "trade_logs/trades_valides.json"
FICHIER_HISTORIQUE = "trade_logs/historique_trades.csv"
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # 🔐 À remplacer
TELEGRAM_CHAT_ID = "675564258"

# === OUTILS ===
def envoyer_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        requests.post(url, data=data)
    except Exception as e:
        st.error(f"Erreur Telegram : {e}")

def ajouter_log_execution(trade):
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
    if os.path.exists(FICHIER_HISTORIQUE):
        df.to_csv(FICHIER_HISTORIQUE, mode='a', header=False, index=False)
    else:
        df.to_csv(FICHIER_HISTORIQUE, index=False)

def charger_trades():
    if os.path.exists(FICHIER_TRADES):
        with open(FICHIER_TRADES, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def supprimer_trade(index):
    trades = charger_trades()
    del trades[index]
    with open(FICHIER_TRADES, "w", encoding="utf-8") as f:
        json.dump(trades, f, indent=2)

def reanalyser_signal(symbol):
    df = pd.DataFrame({
        "datetime": pd.date_range(end=datetime.now(), periods=30, freq="min"),
        "close": [1.1 + 0.001 * i for i in range(30)]
    })
    df_indics = calculer_tous_les_indicateurs(df)
    return analyser_avec_ia(df_indics.tail(1).to_dict(orient="records")[0])

# === EXECUTION ===
trades = charger_trades()

if not trades:
    st.info("Aucun trade validé en attente.")
else:
    for i, trade in enumerate(trades):
        st.markdown("---")
        st.markdown(f"### 🎯 {trade['symbol']} - {trade['direction']} - {trade['mise']}$ - {trade['duree']}s")
        st.markdown(f"🧠 Confiance IA initiale : {trade.get('confiance', '-')}")
        if st.button(f"🔍 Vérifier maintenant (#{i+1})"):
            new_check = reanalyser_signal(trade['symbol'])
            st.markdown(f"🧠 Nouvelle décision IA : **{new_check['decision']}** — Confiance : **{new_check['confiance']}**")
            if new_check["decision"] == trade["direction"]:
                if st.button(f"✅ Exécuter ce trade (#{i+1}) après validation IA"):
                    resultat = executer_trade(
                        symbole=trade['symbol'],
                        direction=trade['direction'],
                        strategie="IA_VALIDÉE",
                        resultat="réexaminé",
                        volume=trade['mise'],
                        expiration=trade['duree']
                    )
                    ajouter_log_execution(trade)
                    envoyer_telegram(f"🚀 Trade exécuté : {trade['symbol']} | {trade['direction']} | {trade['mise']}$ | {trade['duree']}s ✅")
                    st.success("✅ Trade exécuté et logué.")
                    supprimer_trade(i)
            else:
                st.error("❌ L'IA actuelle ne valide plus cette direction.")
        elif st.button(f"❌ Rejeter ce trade (#{i+1})"):
            supprimer_trade(i)
            st.warning("Trade supprimé.")

# === HISTORIQUE DES TRADES ===
st.markdown("---")
st.header("📈 Historique des trades exécutés")
if os.path.exists(FICHIER_HISTORIQUE):
    df_hist = pd.read_csv(FICHIER_HISTORIQUE)
    st.dataframe(df_hist)
else:
    st.info("Aucun trade n’a encore été exécuté.")
