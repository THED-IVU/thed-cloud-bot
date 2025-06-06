# 📄 main_launcher.py – Lancement central du Bot IA TIB avec Guardian, Copilote, WebSocket & Logs

import subprocess
import threading
import streamlit as st
import json
import os
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from core.forex_manager import cloture_auto_si_tp_sl
from core.init_mt5_connection import get_prix_reel

# 🧠 Test IA
from ia_alerts import envoyer_alerte_ia
from ia_storage import sauvegarder_analyse, sync_to_firebase

st.set_page_config(page_title="TIB Launcher - IA & Guardian", layout="centered")
st.title("🤖 Lancement central du Bot IA - THED_IVU_BOT")

# ⏱️ Rafraîchissement automatique toutes les 30 secondes
st_autorefresh(interval=30 * 1000, key="cloture_auto_refresh")

# ------------------- Initialisation de session -------------------
for state_key in ["guardian_started", "bot_started", "controle_started", "ws_receiver_started", "scheduler_started"]:
    if state_key not in st.session_state:
        st.session_state[state_key] = False

st.markdown("## 🧠 Modules disponibles")

# ------------------- 1. Lancement Guardian IA -------------------
if st.button("🧠 Démarrer Guardian IA", type="primary") and not st.session_state.guardian_started:
    def launch_guardian():
        subprocess.Popen(["python", "ai_guardian.py"])
    threading.Thread(target=launch_guardian).start()
    st.session_state.guardian_started = True
    st.success("✅ TIB Guardian lancé avec succès")

# ------------------- 2. Lancement Interface Copilote -------------------
if st.button("🚀 Lancer Interface Copilote IA", type="primary") and not st.session_state.bot_started:
    def launch_bot():
        subprocess.Popen(["streamlit", "run", "pages/6_PocketOption_Copilote.py"])
    threading.Thread(target=launch_bot).start()
    st.session_state.bot_started = True
    st.success("✅ Interface Copilote lancée")

# ------------------- 3. Interface contrôle IA Guardian -------------------
if st.button("🛡️ Lancer Panneau de Contrôle Guardian", type="secondary") and not st.session_state.controle_started:
    def launch_controle():
        subprocess.Popen(["streamlit", "run", "pages/7_Guardian_IA_Control.py", "--server.port", "8503"])
    threading.Thread(target=launch_controle).start()
    st.session_state.controle_started = True
    st.success("🛡️ Panneau de contrôle lancé sur : http://localhost:8503")

# ------------------- 3.bis. Lancer Analyse Stratégique IA -------------------
if st.button("🧠 Lancer Analyse Stratégique IA", type="secondary"):
    try:
        from core.ai_guardian import GuardianStrategique
        guardian = GuardianStrategique()
        resultat = guardian.evaluer_strategie("forex", "1j", "professionnel")
        st.success("✅ Analyse stratégique IA effectuée.")
        st.json(resultat)
    except Exception as e:
        st.error(f"❌ Erreur dans l’analyse stratégique : {e}")

# ------------------- 4. Lancement Récepteur WebSocket -------------------
if st.button("🔌 Activer Réception Signaux WebSocket", type="primary") and not st.session_state.ws_receiver_started:
    def launch_ws_receiver():
        subprocess.Popen(["python", "ws_trade_receiver.py"])
    threading.Thread(target=launch_ws_receiver).start()
    st.session_state.ws_receiver_started = True
    st.success("🔗 Serveur WebSocket en écoute sur ws://localhost:8765")

# ------------------- 5. Suggestions IA internes -------------------
if st.session_state.guardian_started:
    st.markdown("---")
    st.markdown("### 🔒 Suggestions IA en attente de validation")

    suggestions = [
        {"id": "maj_strategy", "texte": "Mettre à jour la stratégie RSI/EMA selon les résultats récents"},
        {"id": "ajout_news", "texte": "Ajouter une nouvelle source d’actualité économique"},
        {"id": "auto_risk", "texte": "Activer le module d’ajustement automatique du risque"},
        {"id": "maj_module_ai", "texte": "Mettre à jour la logique IA avec nouvelles données"}
    ]

    for suggestion in suggestions:
        col1, col2 = st.columns([4, 1])
        col1.markdown(f"📌 {suggestion['texte']}")
        if col2.button("✅ Approuver", key=suggestion["id"]):
            st.success(f"✅ Suggestion '{suggestion['texte']}' validée.")
            os.makedirs("logs", exist_ok=True)
            with open("logs/guardian_actions.log", "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "datetime": datetime.now().isoformat(),
                    "id": suggestion["id"],
                    "texte": suggestion["texte"],
                    "status": "approved"
                }) + "\n")

# ------------------- 6. Auto-Clôture périodique (TP/SL) -------------------
st.markdown("---")
st.markdown("## ⏱️ Vérification automatique TP/SL (30s)")

actifs_surveillance = ["EURUSD", "BTCUSD", "USDJPY", "XAUUSD"]
for actif in actifs_surveillance:
    prix = get_prix_reel(actif)
    if prix:
        msgs = cloture_auto_si_tp_sl(actif, prix)
        for m in msgs:
            st.warning(f"{actif} - {m}")
    else:
        st.error(f"❌ Prix non disponible pour {actif}")

# ------------------- 7. Journalisation des signaux reçus -------------------
st.markdown("---")
st.markdown("## 📊 Derniers signaux IA reçus (WebSocket)")

log_file_path = "logs/received_trades.log"
if os.path.exists(log_file_path):
    with open(log_file_path, "r", encoding="utf-8") as f:
        logs = f.readlines()[-5:]
    for line in reversed(logs):
        try:
            data = json.loads(line)
            st.info(f"{data.get('symbol', '??')} | {data.get('direction', '?')} | "
                    f"{data.get('mise', '?')}$ | {data.get('duree', '?')}s | Score : {data.get('score', '?')}%")
        except Exception:
            st.warning("❌ Ligne corrompue dans le fichier log.")
else:
    st.warning("Aucun signal reçu pour le moment. Active le module WebSocket ci-dessus.")

# ------------------- 8. 🧪 Bouton de test global IA (Firebase + Alerte + SQLite) -------------------
st.markdown("---")
st.markdown("## 🧪 Test complet des fonctions IA")

if st.button("🚀 Lancer test global IA (alerte + Firebase + SQLite)"):
    try:
        resultat_test = {
            "horodatage": datetime.now().isoformat(),
            "source": "test_launcher",
            "marche": "BTCUSD",
            "horizon": "30min",
            "niveau": "expert",
            "prediction": "Hausse probable à court terme",
            "recommandation": "Acheter au-dessus de 67 500$",
            "score_confiance": 91
        }
        envoyer_alerte_ia(resultat_test)
        sauvegarder_analyse("test_launcher", resultat_test)
        sync_to_firebase("test_launcher", resultat_test)
        st.success("✅ Test complet IA effectué avec succès.")
    except Exception as e:
        st.error(f"❌ Erreur pendant le test IA : {e}")

# ------------------- 9. Démarrage automatique du scheduler -------------------
if not st.session_state.scheduler_started:
    def auto_scheduler():
        subprocess.Popen(["python", "guardian_scheduler.py"])
    threading.Thread(target=auto_scheduler).start()
    st.session_state.scheduler_started = True

# ------------------- Footer -------------------
st.markdown("---")
st.caption("🔐 TIB Launcher v1.0 – Contrôle centralisé IA, Guardian & exécution WebSocket – THED_IVU_BOT")
