# 6_PocketOption_Copilote.py – Interface IA Multi-fenêtres Pocket Option (Binaires / Forex)

import streamlit as st
import pandas as pd
import json
import os
import sys
import asyncio
import websockets
from guardian.guardian_multi_validate import lancer_interface_multi_validation
lancer_interface_multi_validation()
from datetime import datetime
from streamlit.components.v1 import html

st.set_page_config(page_title="Copilote IA Pocket Option - Multi-Fenêtres", layout="wide")

# 🔐 Authentification
CORRECT_PASSWORD = "19876Slymthed@"
if "auth_ok" not in st.session_state:
    st.session_state.auth_ok = False
if not st.session_state.auth_ok:
    mdp = st.text_input("🔐 Entrez le mot de passe :", type="password")
    if mdp == CORRECT_PASSWORD:
        st.session_state.auth_ok = True
        st.success("✅ Accès autorisé")
    else:
        st.stop()

# 🔁 Toggle IA global
if "ia_active" not in st.session_state:
    st.session_state.ia_active = False
st.session_state.ia_active = st.toggle("🚀 Lancer l’IA (Auto-exécution des signaux)", value=st.session_state.ia_active)

# Imports internes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.indicators import calculer_tous_les_indicateurs
from ai import analyser_avec_ia
from core.learning_tracker import enregistrer_resultat
from core.alert_bot import envoyer_alerte
from core.pocket_executor import executer_trade_binaires
from core.pocket_executor_forex import executer_trade_forex
from core.news_fetcher import get_latest_news
from websocket.ws_trade_sender import envoyer_ordre_async
from notifications.telegram_alert import envoyer_alerte_telegram
from core.pocket_interface_manager import get_config_par_fenetre

# 🔐 Guardian Auto-Fix (AJOUTÉ)
from guardian.guardian_auto_fix import lancer_guardian_auto_fix

if st.sidebar.button("🛡️ Lancer Guardian Auto-Fix"):
    lancer_guardian_auto_fix()

st.title("🧐 Copilote IA - Pocket Option (Multi-fenêtres)")

mode_global = st.selectbox("🎮 Mode de trading", ["BINAIRE", "FOREX"], index=0)
nb_fenetres = st.slider("🪟 Nombre de fenêtres à analyser", 1, 4, 2)

for i in range(nb_fenetres):
    st.subheader(f"🧠 Fenêtre IA n°{i+1}")
    config_fenetre = get_config_par_fenetre(i + 1)
    symbol = config_fenetre.get("symbol", "EURUSD")
    window_id = config_fenetre.get("window_id", f"F{i+1}")

    df = pd.DataFrame({
        "datetime": pd.date_range(end=datetime.now(), periods=30, freq="min"),
        "close": [1.1 + 0.001 * i for i in range(30)],
        "high": [1.1 + 0.0015 * i for i in range(30)],
        "low": [1.1 + 0.0005 * i for i in range(30)]
    })

    df_indics = calculer_tous_les_indicateurs(df)
    resultats_ia = analyser_avec_ia(df_indics.tail(1))

    direction = resultats_ia.get("ACTION", "HOLD").lower()
    confiance = resultats_ia.get("SCORE", "N/A")
    contexte = resultats_ia.get("CONTEXTE", "Indéterminé")

    st.info(f"📊 IA : {direction.upper()} | Score : {confiance}% | Contexte : {contexte}")

    trade_info = {
        "datetime": datetime.now().isoformat(),
        "symbol": symbol,
        "direction": direction,
        "confiance": confiance,
        "contexte": contexte,
        "window": window_id,
        "mode": "auto" if st.session_state.ia_active else "manuel"
    }

    if mode_global == "BINAIRE":
        mise = st.slider(f"💰 Mise ({window_id})", 1, 100, 5, key=f"mise_{i}")
        duree = st.selectbox(f"⏱ Durée ({window_id})", [30, 60, 120], key=f"duree_{i}")
        trade_info.update({"mise": mise, "duree": duree})
    else:
        lot = st.number_input(f"🪙 Lot ({window_id})", min_value=0.01, value=0.05, step=0.01, key=f"lot_{i}")
        leverage = st.selectbox(f"⚙️ Levier ({window_id})", [25, 50, 100, 200], key=f"lev_{i}")
        tp = st.number_input(f"🎯 Take Profit ({window_id})", min_value=0.0, value=1.5, step=0.1, key=f"tp_{i}")
        sl = st.number_input(f"🛑 Stop Loss ({window_id})", min_value=0.0, value=1.0, step=0.1, key=f"sl_{i}")
        trade_info.update({"lot": lot, "leverage": leverage, "tp": tp, "sl": sl})

    if st.session_state.ia_active:
        if mode_global == "BINAIRE":
            executer_trade_binaires(trade_info)
        else:
            executer_trade_forex(trade_info)
        with open("logs/ia_signals.log", "a", encoding="utf-8") as f:
            f.write(json.dumps(trade_info) + "\n")
        st.success(f"✅ Trade IA auto exécuté ({window_id})")
        enregistrer_resultat(trade_info, {"status": "envoyé"})
        envoyer_alerte(trade_info, {"status": "envoyé"})
        envoyer_alerte_telegram(trade_info, f"🚀 Trade {mode_global} IA exécuté")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button(f"✅ Valider manuellement ({window_id})", key=f"valider_{i}"):
            if mode_global == "BINAIRE":
                executer_trade_binaires(trade_info)
            else:
                executer_trade_forex(trade_info)
            with open("logs/ia_signals.log", "a", encoding="utf-8") as f:
                f.write(json.dumps(trade_info) + "\n")
            enregistrer_resultat(trade_info, {"status": "envoyé"})
            envoyer_alerte(trade_info, {"status": "envoyé"})
            envoyer_alerte_telegram(trade_info, f"🚀 Trade manuel {mode_global}")
            st.success(f"✅ Trade manuel exécuté ({window_id})")

    with col2:
        if st.button(f"❌ Rejeter ({window_id})", key=f"rejeter_{i}"):
            st.warning("❌ Signal rejeté")

    with col3:
        if st.button(f"🎯 Voir popup IA ({window_id})", key=f"popup_{i}"):
            try:
                rsi = df_indics["RSI"].iloc[-1]
                ema9 = df_indics["EMA_9"].iloc[-1]
                ema21 = df_indics["EMA_21"].iloc[-1]
                macd = df_indics["MACD"].iloc[-1]
                signal = df_indics["MACD_signal"].iloc[-1]
                resume_technique = f"RSI={rsi:.1f}, EMA9={ema9:.4f}, EMA21={ema21:.4f}, MACD={'HAUSSIER' if macd > signal else 'BAISSIER'}"
                resume_fondamentale = get_latest_news(symbol)
                with open("popup_modal_ia.html", "r", encoding="utf-8") as f:
                    popup_html = (
                        f.read()
                        .replace("{direction}", direction)
                        .replace("{confiance}", str(confiance))
                        .replace("{mise}", str(trade_info.get('mise', trade_info.get('lot', 0.01))) )
                        .replace("{duree}", str(trade_info.get('duree', trade_info.get('tp', 60))))
                        .replace("{resume_technique}", resume_technique)
                        .replace("{resume_fondamentale}", resume_fondamentale)
                    )
                    html(popup_html, height=650)
            except Exception as e:
                st.error(f"❌ Erreur popup IA : {e}")

    with st.expander(f"🧾 Historique & Clôture ({window_id})"):
        if st.button(f"🛑 Forcer la clôture Forex ({window_id})", key=f"close_{i}"):
            from core.forex_manager import cloturer_trade_forex
            msg = cloturer_trade_forex(symbol)
            st.warning(msg)
        try:
            with open("logs/ia_signals.log", "r", encoding="utf-8") as f:
                lignes = f.readlines()
            lignes_fenetre = [json.loads(l) for l in lignes if f'"window": "{window_id}"' in l]
            if lignes_fenetre:
                df_historique = pd.DataFrame(lignes_fenetre)
                st.dataframe(df_historique.tail(10))
        except Exception as e:
            st.error(f"Erreur historique : {e}")

with st.expander("🧪 Console IA / JS"):
    st.code(resultats_ia, language="json")
