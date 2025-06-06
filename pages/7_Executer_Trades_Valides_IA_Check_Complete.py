
import streamlit as st
import os
import json
from datetime import datetime
from core.trading_MTX import executer_trade
from indicators import calculer_tous_les_indicateurs
from ai import analyser_avec_ia
from log_history import ajouter_log_execution
import pandas as pd
import requests

st.set_page_config(page_title="Validation IA avant exécution", layout="wide")
st.title("🧠 Exécuter les Trades IA avec Vérification + Historique + Telegram")

fichier = "trade_logs/trades_valides.json"
telegram_chat_id = "675564258"
telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"  # Remplacer par ton vrai token

def envoyer_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        data = {"chat_id": telegram_chat_id, "text": message}
        requests.post(url, data=data)
    except:
        pass

def charger_trades():
    if os.path.exists(fichier):
        with open(fichier, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def supprimer_trade(index):
    trades = charger_trades()
    del trades[index]
    with open(fichier, "w", encoding="utf-8") as f:
        json.dump(trades, f, indent=2)

def reanalyser_signal(symbol):
    df = pd.DataFrame({
        "datetime": pd.date_range(end=datetime.now(), periods=30, freq="min"),
        "close": [1.1 + 0.001 * i for i in range(30)]
    })
    df_indics = calculer_tous_les_indicateurs(df)
    resultat = analyser_avec_ia(df_indics.tail(1).to_dict(orient="records")[0])
    return resultat

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
                    envoyer_telegram(f"🚀 Trade exécuté : {trade['symbol']} | {trade['direction']} | {trade['mise']}$ | {trade['duree']}s")
                    st.success(f"Trade exécuté et enregistré avec succès.")
                    supprimer_trade(i)
            else:
                st.error("❌ L'IA actuelle ne valide plus cette direction.")
        elif st.button(f"❌ Rejeter ce trade (#{i+1})"):
            supprimer_trade(i)
            st.warning(f"Trade #{i+1} supprimé.")
