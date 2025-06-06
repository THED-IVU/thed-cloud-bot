import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Initialisation des paramètres adaptatifs (avec défauts)
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
            "TP": 0.002,  # Take profit = +0.2%
            "SL": 0.001   # Stop loss = -0.1%
        }

def save_params(params):
    with open("params.json", "w") as f:
        json.dump(params, f)

params = load_params()

# Interface
st.sidebar.title("⚙️ Paramètres actifs")
st.sidebar.write(f"RSI_length = {params['RSI_length']}")
st.sidebar.write(f"MACD = ({params['MACD_fast']}, {params['MACD_slow']})")
st.sidebar.write(f"SMA = ({params['SMA_short']}, {params['SMA_long']})")
st.sidebar.write(f"TP = {params['TP']*100:.2f}% | SL = {params['SL']*100:.2f}%")

# Historique des trades simulés (session)
if "trade_history" not in st.session_state:
    st.session_state.trade_history = []

# Simulation de trade (exemple)
if st.button("Simuler un trade gagnant"):
    price = 1.1000
    result = {
        "datetime": datetime.now().isoformat(),
        "action": "BUY",
        "price": price,
        "result": "win",
        "gain": price * params["TP"],
        "asset": "SIMULATION",
        **params
    }
    st.session_state.trade_history.append(result)

if st.button("Simuler un trade perdant"):
    price = 1.1000
    result = {
        "datetime": datetime.now().isoformat(),
        "action": "SELL",
        "price": price,
        "result": "loss",
        "gain": -price * params["SL"],
        "asset": "SIMULATION",
        **params
    }
    st.session_state.trade_history.append(result)

# Historique affiché
st.subheader("📄 Historique de trades")
df_hist = pd.DataFrame(st.session_state.trade_history)
if not df_hist.empty:
    st.dataframe(df_hist.tail(10))

    # Calcul performance
    win_rate = (df_hist['result'] == 'win').mean()
    total_gain = df_hist['gain'].sum()
    st.metric("Taux de réussite", f"{win_rate*100:.1f}%")
    st.metric("Gain net simulé", f"{total_gain:.5f} $")

    # Ajustement si mauvais score
    if len(df_hist) >= 10 and win_rate < 0.5:
        st.warning("Performance faible : ajustement automatique...")
        params["RSI_length"] = min(params["RSI_length"] + 1, 21)
        params["SMA_short"] = max(params["SMA_short"] - 2, 10)
        save_params(params)
        st.rerun()
else:
    st.info("Aucun trade simulé pour l'instant.")
