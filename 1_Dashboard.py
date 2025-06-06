import streamlit as st
from datetime import datetime

st.set_page_config(page_title="📊 THED BOT – Menu Principal", layout="wide")

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Accéder à :", [
    "🏠 Accueil",
    "📈 Dashboard IA",
    "📈 Résultats IA + Patterns",
    "📉 Historique IA + Patterns",
    "🧠 Admin IA",
    "📊 Stratégies",
    "📊 Rapport IA",
    "📚 Mémoire IA",
    "📂 Contextes & Échecs IA",
    "📈 Stats Contextes",
    "🧠 IA Heatmap & Erreurs",
    "🧠 IA Corrective",
    "⚙️ Config IA",
    "📊 Patterns Détectés"
])

if page == "🏠 Accueil":
    st.title("🤖 Bienvenue sur le THED IVU BOT")
    st.markdown("""
    - Suivi IA en temps réel
    - Visualisation des patterns
    - Résultats enrichis avec chandeliers
    - Config IA dynamique et évolutive
    """)

elif page == "📈 Dashboard IA":
    st.switch_page("pages/2_Dashboard_IA.py")

elif page == "📈 Résultats IA + Patterns":
    st.switch_page("pages/Dashboard_IA_Resultats.py")

elif page == "📉 Historique IA + Patterns":
    st.switch_page("pages/historique_ia_patterns.py")

elif page == "🧠 Admin IA":
    st.switch_page("pages/Admin_IA.py")

elif page == "📊 Stratégies":
    st.markdown("### 📁 Liste des stratégies intégrées")
    st.markdown("- EMA + RSI")
    st.markdown("- Heikin + PSAR")
    st.markdown("- Fibonacci + Bougies")
    st.markdown("- Sniper IA")
    st.markdown("- Candlestick")

elif page == "📊 Rapport IA":
    st.switch_page("pages/Rapport_IA.py")

elif page == "📚 Mémoire IA":
    st.switch_page("pages/Admin_IA_Memory.py")

elif page == "📂 Contextes & Échecs IA":
    st.switch_page("pages/Admin_IA_Contextes.py")

elif page == "📈 Stats Contextes":
    st.switch_page("pages/Admin_IA_Stats.py")

elif page == "🧠 IA Heatmap & Erreurs":
    st.switch_page("pages/Admin_IA_Heatmap.py")

elif page == "🧠 IA Corrective":
    st.switch_page("pages/Admin_IA_Corrective.py")

elif page == "⚙️ Config IA":
    st.switch_page("pages/Admin_IA_Config.py")

elif page == "📊 Patterns Détectés":
    st.switch_page("pages/Admin_IA_Patterns.py")