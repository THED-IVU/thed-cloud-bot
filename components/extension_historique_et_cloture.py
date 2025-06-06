
import streamlit as st
import json
import pandas as pd
from core.forex_manager import cloturer_trade_forex

def afficher_historique_et_cloture(symbol, window_id):
    if st.button(f"🛑 Forcer la clôture Forex ({window_id})", key=f"close_{window_id}"):
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
