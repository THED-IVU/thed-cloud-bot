# ✅ guardian_scheduler.py – Superviseur intelligent unifié (interface uniquement)

# 🔁 Ajouter automatiquement le dossier de base au sys.path
import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from utils.path_utils import ajouter_base_et_sous_dossiers
ajouter_base_et_sous_dossiers(["notifications", "core", "utils", "MON_API_PRO", "ia", "guardian"])

# === Imports principaux ===
import time
import signal
import subprocess
import datetime
import json
import streamlit as st
import schedule

# === Modules internes Guardian ===
from guardian_scanner import scanner_complet
from guardian_suggestions import generer_suggestions
from guardian_executor import executer_correctifs
from guardian_reporter import enregistrer_rapport_json, enregistrer_rapport_pdf
from telegram_alert import envoyer_alerte_guardian
from email_cron import generer_contenu_html_guardian, envoyer_email_rapport

# 🔁 Firebase + GitHub + IA
from core.firebase_sync import push_ia_decision_to_firebase, push_trade_to_firebase
from ia_strategique import analyser_contexte
from ia_storage import sauvegarder_analyse as sauvegarder_resultat
from git_sync import push_to_github

# === CONFIGURATION ===
INTERVAL_HEURES = 6
INTERVAL_SECONDES = INTERVAL_HEURES * 3600
PROCESS_KEY = "guardian_pid"

# === TÂCHE COMPLÈTE FUSIONNÉE ===
def tache_complete():
    horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{horodatage}] 🧠 Lancement de la tâche Guardian complète...")

    try:
        rapport = scanner_complet(".")
        suggestions = generer_suggestions(rapport)
        correctifs = [s for s in suggestions if s.get("impact", 100) >= 50]

        if correctifs:
            resultats = executer_correctifs(correctifs)
            fichier = f"auto_guardian_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            enregistrer_rapport_json(resultats, fichier)
            enregistrer_rapport_pdf(resultats, fichier)
            envoyer_alerte_guardian(resultats)
            contenu = generer_contenu_html_guardian(resultats)
            envoyer_email_rapport("📊 Rapport Auto – Guardian IA", contenu)
            print(f"[{horodatage}] ✅ Correctifs appliqués et alertes envoyées.")
        else:
            print(f"[{horodatage}] ✅ Aucun correctif requis.")
    except Exception as e:
        print(f"[{horodatage}] ❌ Erreur dans le module Guardian : {e}")

    try:
        print(f"[{horodatage}] 🧠 Analyse IA stratégique...")
        resultat = analyser_contexte(marche="forex", horizon="1j", niveau="professionnel", source="auto")
        sauvegarder_resultat(resultat, source="auto")
        push_ia_decision_to_firebase("forex_global", resultat)
        print(f"[{horodatage}] ✅ Analyse IA sauvegardée.")
    except Exception as e:
        print(f"[{horodatage}] ❌ Erreur dans l’analyse IA : {e}")

    try:
        print(f"[{horodatage}] ☁️ Synchronisation Firebase...")
        print(f"[{horodatage}] ✅ Firebase activé via core/firebase_sync.py")
    except Exception as e:
        print(f"[{horodatage}] ❌ Erreur Firebase : {e}")

    try:
        print(f"[{horodatage}] 📤 Push GitHub...")
        push_to_github()
        print(f"[{horodatage}] ✅ Code mis à jour sur GitHub.")
    except Exception as e:
        print(f"[{horodatage}] ❌ Erreur GitHub : {e}")

    print(f"[{horodatage}] 💤 Prochaine exécution dans {INTERVAL_HEURES}h...\n")

# 🔁 Scheduler planifié (non utilisé ici mais gardé pour référence)
schedule.every(INTERVAL_HEURES).hours.do(tache_complete)

# === INTERFACE STREAMLIT UNIQUEMENT ===
def lancer_interface_streamlit():
    st.set_page_config(page_title="🛡️ Planificateur Guardian Fusionné", layout="centered")

    with st.spinner("Chargement de Guardian IA..."):
        time.sleep(1)

    # ☁️ Connexion automatique à Firebase dès l'ouverture
    try:
        push_trade_to_firebase({"test": "connexion_streamlit"})
        st.success("☁️ Connexion Firebase réussie.")
    except Exception as e:
        st.warning(f"⚠️ Firebase non connecté : {e}")

    st.title("🛡️ Guardian IA – Planificateur & Supervision")
    st.markdown("Cette interface permet de **surveiller automatiquement le bot**, d'**analyser le marché**, d'**appliquer des correctifs IA** et de **synchroniser Firebase & GitHub** toutes les 6h.")

    if PROCESS_KEY not in st.session_state:
        st.session_state[PROCESS_KEY] = None

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("▶️ Lancer tâche IA maintenant"):
            st.warning("⏳ Tâche complète en cours...")
            tache_complete()
            st.success("✅ Tâche complète terminée.")

    with col2:
        st.info("Utilise `guardian_launcher.py` pour exécuter en console.")

    with col3:
        if st.button("🔁 Recharger manuellement"):
            st.rerun()

# === FORÇAGE INTERFACE STREAMLIT ===
lancer_interface_streamlit()
