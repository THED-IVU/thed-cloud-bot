# 📄 Interface Streamlit de contrôle IA Guardian – BOT_MT5_THED_PRO

import streamlit as st
import json
import os
from datetime import datetime

LOG_FILE = "logs/guardian_actions.log"
SUGGESTIONS = [
    {"id": "maj_strategy", "texte": "Mettre à jour RSI/EMA selon les résultats récents"},
    {"id": "ajout_news", "texte": "Ajouter une source d’actualités économiques"},
    {"id": "auto_risk", "texte": "Activer le module d’ajustement automatique du risque"},
    {"id": "maj_module_ai", "texte": "Mettre à jour la logique IA avec nouvelles données"},
]

st.set_page_config(page_title="👁️ TIB Guardian - Contrôle IA", layout="centered")
st.title("🧠 Centre de Commande - Guardian IA")

st.markdown("#### 📌 Suggestions IA en attente de validation")

for suggestion in SUGGESTIONS:
    col1, col2 = st.columns([4, 1])
    col1.markdown(f"📍 {suggestion['texte']}")
    if col2.button("✅ Approuver", key=suggestion["id"]):
        st.success(f"✅ Suggestion '{suggestion['texte']}' validée.")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "datetime": datetime.now().isoformat(),
                "id": suggestion["id"],
                "texte": suggestion["texte"],
                "status": "approved"
            }) + "\n")

st.markdown("---")
st.markdown("#### 📁 Historique des validations")
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.readlines()[-10:]  # dernières 10 entrées
        for log in logs:
            item = json.loads(log)
            st.markdown(f"- 🗓️ {item['datetime']} : **{item['texte']}** → ✅ Validé")
else:
    st.info("Aucune action encore validée.")
