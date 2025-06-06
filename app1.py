import streamlit as st
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt
from openai import OpenAI
import os
import json
from datetime import datetime
from core.firebase_logger import envoyer_log_firebase
envoyer_log_firebase(
    plateforme="MT5",
    action="Backtest terminé",
    resultat="gagné",
    strategie="EMA_RSI"
)


# ---------- PARAMS JSON CHARGE ET CONTROLES MANUELS ----------

def load_params():
    try:
        with open("params.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "RSI_length": 14,
            "MACD_fast": 12,
            "MACD_slow": 26,
            "SMA_short": 20,
            "SMA_long": 50,
            "TP": 0.002,
            "SL": 0.001
        }

def save_params(params):
    with open("params.json", "w") as f:
        json.dump(params, f)

params = load_params()

# UI pour ajuster manuellement les paramètres dans la sidebar
st.sidebar.title("⚙️ Paramètres actifs (manuel + auto)")
params["RSI_length"] = st.sidebar.slider("RSI Length", 7, 21, params["RSI_length"])
params["MACD_fast"] = st.sidebar.slider("MACD Fast", 5, 15, params["MACD_fast"])
params["MACD_slow"] = st.sidebar.slider("MACD Slow", 20, 30, params["MACD_slow"])
params["SMA_short"] = st.sidebar.slider("SMA Court Terme", 10, 30, params["SMA_short"])
params["SMA_long"] = st.sidebar.slider("SMA Long Terme", 40, 100, params["SMA_long"])
params["TP"] = st.sidebar.number_input("Take Profit (%)", value=params["TP"]*100, step=0.05)/100
params["SL"] = st.sidebar.number_input("Stop Loss (%)", value=params["SL"]*100, step=0.05)/100

save_params(params)

# ---------- SESSION STATE ----------
if "trade_history" not in st.session_state:
    st.session_state.trade_history = []

client = OpenAI(api_key="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")

st.title("📈 BotTHEDIVU")
symbol = "EURUSD=X"
interval = "1m"
period = "5d"

st.info("Chargement des données...")
data = yf.download(symbol, interval=interval, period=period)
data = data.dropna()
data.columns = ["_".join(col).lower() if isinstance(col, tuple) else col.lower() for col in data.columns]

st.write("Colonnes disponibles :", data.columns.tolist())
data['RSI'] = ta.rsi(data['close_eurusd=x'], length=params["RSI_length"])
macd = ta.macd(data['close_eurusd=x'], fast=params["MACD_fast"], slow=params["MACD_slow"])
data = pd.concat([data, macd], axis=1)
data['SMA20'] = ta.sma(data['close_eurusd=x'], length=params["SMA_short"])
data['SMA50'] = ta.sma(data['close_eurusd=x'], length=params["SMA_long"])

# ---------- STRATÉGIE TECHNIQUE ----------
data['signal'] = ""
data.loc[(data['RSI'] < 30) & (data['MACD_12_26_9'] > data['MACDs_12_26_9']) & (data['SMA20'] > data['SMA50']), 'signal'] = "BUY"
data.loc[(data['RSI'] > 70) & (data['MACD_12_26_9'] < data['MACDs_12_26_9']) & (data['SMA20'] < data['SMA50']), 'signal'] = "SELL"

st.subheader("📉 Graphique des prix avec signaux")
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(data['close_eurusd=x'], label='Prix', color='black')
ax.plot(data['SMA20'], label='SMA20', linestyle='--')
ax.plot(data['SMA50'], label='SMA50', linestyle='--')
buy_signals = data[data['signal'] == 'BUY']
sell_signals = data[data['signal'] == 'SELL']
ax.scatter(buy_signals.index, buy_signals['close_eurusd=x'], marker='^', color='green', label='BUY')
ax.scatter(sell_signals.index, sell_signals['close_eurusd=x'], marker='v', color='red', label='SELL')
ax.legend()
st.pyplot(fig)

# ---------- GPT + TRADING SIMULÉ ----------
st.subheader("🤖 Analyse IA (GPT)")
latest = data[['close_eurusd=x', 'RSI', 'MACD_12_26_9', 'MACDs_12_26_9', 'SMA20', 'SMA50', 'signal']].tail(5)
summary = latest.to_string()

prompt = f"""
Voici un extrait de données de marché sur EUR/USD :

{summary}

Donne une analyse brève :
- La tendance générale (haussière, baissière, neutre)
- Si un trade BUY ou SELL est envisageable
- Les risques associés
- Une note sur 10 sur la qualité du signal actuel

Format de réponse : TENDANCE / ACTION / RISQUES / NOTE
"""

if st.button("📤 Lancer l'analyse IA"):
    with st.spinner("Consultation du cerveau GPT..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un expert en analyse technique de marché Forex."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content

        st.subheader("📊 Résultat de l'analyse IA")
        st.markdown(result)
        st.info(f"🔎 Dernier signal : {data.iloc[-1]['signal']} | Prix actuel : {data.iloc[-1]['close_eurusd=x']:.5f}")

        if "buy" in result.lower() or "sell" in result.lower():
            action = "BUY" if "buy" in result.lower() else "SELL"
            if st.button(f"🚀 Exécuter le trade {action} ?"):
                last_row = data.iloc[-1]
                next_row = data.iloc[-2]
                entry_price = last_row['close_eurusd=x']
                exit_price = next_row['close_eurusd=x']
                profit = (exit_price - entry_price) if action == "BUY" else (entry_price - exit_price)

                trade = {
                    "datetime": last_row.name,
                    "action": action,
                    "price": entry_price,
                    "exit_price": exit_price,
                    "profit": profit,
                    "RSI": last_row['RSI'],
                    "MACD": last_row['MACD_12_26_9'],
                    "MACDs": last_row['MACDs_12_26_9'],
                    "SMA20": last_row['SMA20'],
                    "SMA50": last_row['SMA50'],
                    "source": "IA + Technique"
                }

                st.session_state.trade_history.append(trade)
                df_trades = pd.DataFrame(st.session_state.trade_history)
                df_trades.to_csv("historique_trades.csv", index=False)
                st.success(f"✅ Le trade {action} a été simulé à {trade['price']:.5f}")
        else:
            st.info("📭 Aucun signal d'action immédiate détecté.")

# ---------- EXPORT CSV ----------
st.subheader("💾 Exporter les signaux")
if st.button("📥 Télécharger les signaux au format CSV"):
    data[data['signal'] != ""].to_csv("signaux_trading.csv")
    st.success("Fichier exporté")

# ---------- HISTORIQUE ET P&L ----------
if st.session_state.trade_history:
    df_hist = pd.DataFrame(st.session_state.trade_history)
    st.subheader("📜 Historique des trades exécutés")
    st.dataframe(df_hist.tail(10))

    st.subheader("📈 P&L cumulé")
    df_hist["P&L_cumul"] = df_hist["profit"].cumsum()
    st.line_chart(df_hist.set_index("datetime")["P&L_cumul"])

    # Stats
    total = df_hist["profit"].sum()
    avg = df_hist["profit"].mean()
    win_rate = (df_hist["profit"] > 0).mean()
    st.markdown(f"""
    **💰 Gain total :** `{total:.5f}`  
    **📈 Trade moyen :** `{avg:.5f}`  
    **✅ Taux de réussite :** `{win_rate*100:.2f}%`
    """)

    if len(df_hist) >= 10 and win_rate < 0.5:
        st.warning("⚠️ Performance faible détectée → ajustement automatique")
        params["RSI_length"] = min(params["RSI_length"] + 1, 21)
        params["SMA_short"] = max(params["SMA_short"] - 2, 10)
        save_params(params)
        st.rerun()
else:
    st.info("Aucun trade exécuté pour l'instant.")
