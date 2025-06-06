# pages/1_Dashboard.py

# 1️⃣ Config visuelle + dynamique (DOIT être tout en haut)
from utils_ui import init_page
CONFIG = init_page("📊 Dashboard Temps Réel")

# 2️⃣ Imports classiques
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from config_state import sidebar_config
from runtime_config import get_runtime_config
from indicators import calculer_tous_les_indicateurs
from scanner import get_active_assets
from trading import lire_trades

# 3️⃣ Barre latérale
sidebar_config()
CONFIG = get_runtime_config()

# 4️⃣ Choix de l'actif à analyser (version dynamique via scanner MT5 ou Yahoo)
actifs = get_active_assets("auto")
actif_choisi = st.selectbox("Choisis un actif à analyser :", actifs)

# 5️⃣ Récupération des données (fallback avec yfinance uniquement si Yahoo symbol)
import yfinance as yf

@st.cache_data(ttl=300)
def get_data(actif):
    try:
        df = yf.download(actif, period="5d", interval="15m")
        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Adj Close': 'adj_close',
            'Volume': 'volume'
        })
        return df
    except Exception as e:
        st.error(f"Erreur de récupération des données : {e}")
        return pd.DataFrame()

df = get_data(actif_choisi)

if not df.empty:
    # 6️⃣ Calcul automatique de tous les indicateurs
    df = calculer_tous_les_indicateurs(df)

    # 7️⃣ Affichage graphique
    st.subheader(f"📈 Indicateurs techniques - {actif_choisi}")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(df.index, df['close'], label='Prix de clôture', linewidth=1)
    ax.plot(df.index, df['ema9'], label='EMA 9')
    ax.plot(df.index, df['ema21'], label='EMA 21')

    for i in df.index:
        if df.loc[i, 'signal'] == "Achat":
            ax.plot(i, df.loc[i, 'close'], marker='^', color='green')
        elif df.loc[i, 'signal'] == "Vente":
            ax.plot(i, df.loc[i, 'close'], marker='v', color='red')

    ax.set_title("📊 Évolution des prix et signaux")
    ax.legend()
    st.pyplot(fig)

    # 8️⃣ Derniers signaux détectés
    st.subheader("🔔 Derniers signaux détectés")
    dernier_signal = df[['close', 'signal']].dropna().tail(5)
    st.dataframe(dernier_signal)

    # 9️⃣ Explications IA des derniers trades (si disponibles)
    st.subheader("🧠 Justifications IA des derniers trades")
    try:
        df_trades = lire_trades()
        df_trades = df_trades[df_trades['asset'] == actif_choisi].copy()
        if not df_trades.empty:
            df_exp = df_trades[['datetime', 'source', 'action', 'note', 'score_ia', 'explication_ia']].tail(5)
            df_exp['datetime'] = pd.to_datetime(df_exp['datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')
            st.dataframe(df_exp, use_container_width=True)
        else:
            st.info("Aucun trade enregistré sur cet actif.")
    except Exception as e:
        st.warning(f"⚠️ Impossible d'afficher les explications IA : {e}")
else:
    st.warning("Aucune donnée disponible pour cet actif.")
