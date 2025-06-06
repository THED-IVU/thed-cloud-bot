# pages/3_Configuration_API.py

import streamlit as st
import requests

st.set_page_config(page_title="Configuration API", layout="centered")

st.title("🛠️ Configuration dynamique du Bot IA")

API_URL = st.text_input("📡 URL de l’API", "http://localhost:5000")

# ---------- Charger la configuration actuelle ---------- #
st.subheader("📥 Paramètres actuels")

if st.button("🔄 Recharger la config"):
    try:
        r = requests.get(f"{API_URL}/get_stats")
        if r.status_code == 200:
            config = r.json()
            st.session_state["config_actuelle"] = config
        else:
            st.error("❌ Erreur de récupération : code " + str(r.status_code))
    except Exception as e:
        st.error(f"Connexion impossible à l’API : {e}")

# ---------- Affichage de la config actuelle ---------- #
if "config_actuelle" in st.session_state:
    conf = st.session_state["config_actuelle"]
    st.json(conf)

# ---------- Mise à jour dynamique ---------- #
st.subheader("✏️ Modifier la configuration")

risk = st.number_input("💰 Risque par trade (%)", 0.01, 0.10, step=0.01, format="%.2f")
sl_pips = st.number_input("🛑 Stop Loss (en pips)", 1, 100, step=1, value=10)
max_loss = st.number_input("❌ Pertes max par jour", 1, 10, step=1, value=3)
max_chain = st.number_input("🔥 Gains max en chaîne", 1, 20, step=1, value=10)
max_trades = st.number_input("📊 Max trades / jour", 1, 50, step=1, value=10)

if st.button("📤 Appliquer les modifications"):
    payload = {
        "risk_per_trade": float(risk),
        "stop_loss_pips": int(sl_pips),
        "max_loss_day": int(max_loss),
        "max_win_chain": int(max_chain),
        "max_trades_per_day": int(max_trades)
    }

    try:
        r = requests.post(f"{API_URL}/set_risk_config", json=payload)
        if r.status_code == 200:
            st.success("✅ Configuration mise à jour avec succès")
            st.session_state["config_actuelle"] = r.json()["new_config"]
        else:
            st.error(f"❌ Échec : code {r.status_code}")
    except Exception as e:
        st.error(f"❌ Erreur de connexion : {e}")

# ---------- Test rapide de stratégie ---------- #
st.write("---")
st.subheader("🚀 Test rapide d'une stratégie")

with st.form("form_test_strat"):
    st.markdown("Saisis un scénario simple et simule une décision IA")

    col1, col2 = st.columns(2)
    with col1:
        test_symbol = st.text_input("Actif", "EURUSD=X")
        test_rsi = st.slider("RSI", 0, 100, value=25)
    with col2:
        test_macd = st.number_input("MACD", -1.0, 1.0, value=0.01, step=0.01)
        test_macds = st.number_input("MACDs", -1.0, 1.0, value=-0.01, step=0.01)

    submitted = st.form_submit_button("🧪 Lancer le test")
    if submitted:
        test_payload = {
            "symbol": test_symbol,
            "rsi": test_rsi,
            "macd": test_macd,
            "macds": test_macds
        }

        try:
            r = requests.post(f"{API_URL}/run_test_strategy", json=test_payload)
            if r.status_code == 200:
                st.success("✅ Résultat du test")
                st.json(r.json())
            else:
                st.error(f"❌ Erreur API : code {r.status_code}")
        except Exception as e:
            st.error(f"❌ Impossible de joindre l'API : {e}")
