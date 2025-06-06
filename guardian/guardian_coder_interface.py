
# guardian/guardian_coder_interface.py

import streamlit as st
import difflib
import os
from guardian_full_scanner import scanner_complet
from guardian_analyzer import analyser_fichier
from guardian_suggestions import generer_suggestions
from guardian_executor import executer_correctifs
from guardian_reporter import enregistrer_rapport_json, enregistrer_rapport_pdf

st.set_page_config(page_title="🧠 Guardian Coder Interface", layout="wide")
st.title("🧠 Interface Visuelle Guardian - Codage & Comparaison")

if st.button("📡 Scanner le projet complet"):
    st.session_state.rapport = scanner_complet(".")
    st.success("✅ Scan terminé")

if "rapport" in st.session_state:
    suggestions = generer_suggestions(st.session_state.rapport)

    st.subheader("🧠 Suggestions détectées")
    for i, s in enumerate(suggestions):
        with st.expander(f"{s['titre']} ({s['impact']}% impact)"):
            path = s["fichier"]
            ancienne_version = ""
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    ancienne_version = f.read()

            nouvelle_version = "# ➕ Version proposée par Guardian\n"
            if s["type"] == "create":
                nouvelle_version += "# Nouveau fichier auto-généré\n\n"
            elif s["type"] == "replace":
                nouvelle_version += "# Remplacement automatique - contenu standard\n\ndef exemple():\n    pass\n"

            # Comparaison texte
            diff = difflib.unified_diff(
                ancienne_version.splitlines(),
                nouvelle_version.splitlines(),
                lineterm=""
            )
            st.code("\n".join(diff), language="diff")

            # Validation
            if st.checkbox(f"✅ Appliquer cette suggestion", key=f"apply_{i}"):
                if "selection" not in st.session_state:
                    st.session_state.selection = []
                st.session_state.selection.append(s)

    if st.button("🚀 Appliquer toutes les corrections validées"):
        if "selection" in st.session_state:
            result = executer_correctifs(st.session_state.selection)
            st.success("🎉 Correctifs appliqués !")
            st.json(result)

            # ➕ Génération de rapport
            path_json = enregistrer_rapport_json(result, "rapport_guardian_coder")
            path_pdf = enregistrer_rapport_pdf(result, "rapport_guardian_coder")

            st.success("📄 Rapports enregistrés !")
            st.markdown(f"📁 Rapport JSON : `{path_json}`")
            st.markdown(f"📁 Rapport PDF : `{path_pdf}`")
        else:
            st.warning("Aucune correction sélectionnée.")
