import streamlit as st
import pandas as pd
from datetime import datetime
from core.indicators import calculer_tous_les_indicateurs
from ai import analyser_avec_ia
from core.pocket_executor import executer_trade_pocket

st.set_page_config(page_title="🧪 Simulateur Multi-Fenêtres", layout="wide")
st.title("🧪 Simulateur de Trading Multi-Graphe")

nb_fenetres = st.selectbox("📊 Nombre de fenêtres à afficher", [1, 2, 3, 4], index=1)

for i in range(nb_fenetres):
    st.subheader(f"🪟 Fenêtre {i+1}")
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        actif = st.selectbox(f"Actif (fenêtre {i+1})", ["EURUSD", "BTCUSD", "ETHUSD"], key=f"actif_{i}")
        mise = st.slider(f"Mise $ (fenêtre {i+1})", 1, 100, 5, key=f"mise_{i}")
    with col2:
        duree = st.selectbox(f"Durée (fenêtre {i+1})", [30, 60, 120], key=f"duree_{i}")
        bouton_auto = st.button(f"🚀 Exécuter automatiquement (fenêtre {i+1})", key=f"auto_{i}")
    with col3:
        bouton_popup = st.button(f"🎯 Voir popup IA (fenêtre {i+1})", key=f"popup_{i}")

    df = pd.DataFrame({
        "datetime": pd.date_range(end=datetime.now(), periods=30, freq="min"),
        "close": [1.1 + 0.001*i for i in range(30)],
        "high": [1.1 + 0.0015*i for i in range(30)],
        "low": [1.1 + 0.0005*i for i in range(30)],
    })

    df_indics = calculer_tous_les_indicateurs(df)
    resultats_ia = analyser_avec_ia(df_indics.tail(1))
    direction = resultats_ia.get("ACTION", "HOLD")
    confiance = resultats_ia.get("SCORE", "N/A")

    if bouton_auto:
        trade_info = {
            "datetime": datetime.now().isoformat(),
            "symbol": actif,
            "direction": direction,
            "confiance": confiance,
            "mise": mise,
            "duree": duree,
            "mode": "auto"
        }
        resultat = executer_trade_pocket(trade_info)
        st.success(f"[Fenêtre {i+1}] ✅ Trade simulé/exécuté : {resultat}")

    if bouton_popup:
        st.info(f"Popup Fenêtre {i+1} : Direction {direction}, Confiance {confiance}, Mise {mise}$, Durée {duree}s")
