# guardian/guardian_multi_validate.py

import streamlit as st
import pandas as pd
import json
from pathlib import Path

# Simuler les données de scan (à remplacer plus tard par lecture automatique des suggestions)
corrections_data = [
    {"Fichier": "core/pocket_executor.py", "Fonctionnalité": "Exécution binaire", "Manquement": "Pas de gestion d'erreur", "Impact": 85},
    {"Fichier": "core/forex_manager.py", "Fonctionnalité": "Clôture Forex", "Manquement": "Aucune vérification d'ordre ouvert", "Impact": 75},
    {"Fichier": "guardian/guardian_scanner.py", "Fonctionnalité": "Scanner IA", "Manquement": "Ignore fichiers dans /deprecated", "Impact": 60},
    {"Fichier": "guardian/guardian_executor.py", "Fonctionnalité": "Correcteur auto", "Manquement": "Ne log pas les corrections", "Impact": 70},
]

st.set_page_config(page_title="Guardian IA – Multi-validation", layout="wide")
st.title("🛡️ Interface de validation Guardian IA")
st.markdown("### 💡 Sélectionne les corrections que Guardian appliquera automatiquement.")

validations = []

for i, correction in enumerate(corrections_data):
    with st.expander(f"🔍 {correction['Fonctionnalité']} ({correction['Fichier']})"):
        st.write(f"📄 **Fichier** : `{correction['Fichier']}`")
        st.write(f"🔧 **Fonctionnalité** : `{correction['Fonctionnalité']}`")
        st.write(f"⚠️ **Manquement détecté** : {correction['Manquement']}")
        st.progress(correction['Impact'] / 100.0)

        approved = st.checkbox("✅ Appliquer cette correction", key=f"validate_{i}")
        if approved:
            validations.append(correction)

if validations:
    st.success(f"✅ {len(validations)} corrections validées. Prêtes à être exécutées par le moteur Guardian.")
    # Sauvegarde temporaire
    output_file = Path("logs/guardian_validations.json")
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(validations, f, indent=2)
    st.code(f"Corrections sauvegardées dans : {output_file}", language="bash")
