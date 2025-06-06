# guardian/guardian_auto_fix.py

import streamlit as st
from guardian_scanner import scanner_rapide
from guardian_full_scanner import scanner_complet
from guardian_suggestions import generer_suggestions
from guardian_executor import executer_correctifs
from guardian_config import charger_config, sauvegarder_config

st.set_page_config(page_title="🛡️ Guardian Auto-Fix", layout="wide")
st.title("🛠️ Guardian IA - Correcteur Automatique")

# Charger configuration
config = charger_config()

# Barre latérale pour configurer le mode
st.sidebar.header("⚙️ Configuration Guardian")
mode_auto = st.sidebar.checkbox("Activer le mode AUTO", value=config.get("mode_auto", False))
niveau_analyse = st.sidebar.selectbox("Niveau d'analyse", ["normal", "avancé"], index=0 if config.get("niveau_analyse") == "normal" else 1)
impact_min = st.sidebar.slider("Seuil d’impact minimal à corriger (%)", 0, 100, config.get("impact_minimal", 50))

# Sauvegarde dynamique
sauvegarder_config({
    "mode_auto": mode_auto,
    "niveau_analyse": niveau_analyse,
    "impact_minimal": impact_min
})

# 🛰️ Choix du type de scan
st.subheader("🔍 Lancer un scan")
scan_type = st.radio("Choisir le type de scan :", ["Rapide (fichiers clés)", "Complet (tout le projet)"])

if st.button("🚀 Démarrer le scan"):
    if scan_type == "Rapide (fichiers clés)":
        rapport = scanner_rapide()
    else:
        rapport = scanner_complet(".")
    st.session_state.rapport = rapport
    st.success("✅ Scan terminé")

# 📋 Affichage du rapport
if "rapport" in st.session_state:
    st.subheader("📋 Rapport d’analyse")
    st.json(st.session_state.rapport)

    suggestions = generer_suggestions(st.session_state.rapport)

    if not suggestions:
        st.info("✅ Aucun correctif nécessaire. Ton bot est clean comme un moine shaolin.")
    else:
        st.subheader("🧠 Suggestions de correction")
        checked_vars = []

        if mode_auto:
            # En mode auto : filtrer automatiquement selon le seuil
            checked_vars = [s for s in suggestions if s.get("impact", 100) >= impact_min]
            st.info(f"🔁 {len(checked_vars)} correctifs sélectionnés automatiquement.")
        else:
            # En mode manuel : proposer la sélection
            for s in suggestions:
                if st.checkbox(f"{s['titre']} - {s['avantage']}", help=s['description']):
                    checked_vars.append(s)

        if checked_vars:
            if st.button("✅ Appliquer les correctifs sélectionnés"):
                result = executer_correctifs(checked_vars)
                st.success("🎉 Correctifs appliqués !")
                st.json(result)
