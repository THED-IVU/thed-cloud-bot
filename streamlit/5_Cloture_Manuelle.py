# 📄 Fichier : streamlit/5_Cloture_Manuelle.py

import streamlit as st
import matplotlib.pyplot as plt
from core.trading_MTX import cloturer_ordre

try:
    import MetaTrader5 as mt5
    MT5_OK = mt5.initialize()
except:
    MT5_OK = False

st.set_page_config(page_title="Clôture manuelle", layout="centered")
st.title("🔒 Forcer la clôture d'une position ouverte")

# 📌 Récupération des positions MT5
positions = []
symbols = []
profit_latent = None

if MT5_OK:
    positions = mt5.positions_get()
    if positions:
        symbols = list(set(pos.symbol for pos in positions))

# 📤 Sélection ou saisie du symbole
if symbols:
    symbol = st.selectbox("Sélectionnez un actif à clôturer", symbols)
else:
    symbol = st.text_input("Entrez le symbole de l'actif ", value="EURUSD")

# 💸 Affichage du profit latent + Graphique SL/TP
if MT5_OK and symbol:
    pos = next((p for p in positions if p.symbol == symbol), None)
    if pos:
        profit_latent = pos.profit
        entry = pos.price_open
        sl = pos.sl
        tp = pos.tp
        st.info(f"💰 Profit latent : {profit_latent:.2f} $")

        fig, ax = plt.subplots()
        ax.axhline(entry, color='blue', label='Entrée')
        if sl > 0:
            ax.axhline(sl, color='red', linestyle='--', label='Stop Loss')
        if tp > 0:
            ax.axhline(tp, color='green', linestyle='--', label='Take Profit')
        ax.set_title(f"{symbol} - SL/TP/Entrée")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("Aucune position détectée sur cet actif.")

# ❌ Bouton de clôture individuelle
if st.button("❌ Clôturer maintenant"):
    result = cloturer_ordre(symbol)
    if result["statut"] == "ok":
        st.success(f"✅ Position sur {symbol} cloturée avec profit : {result['profit']:.2f} $")
    else:
        st.error(f"Erreur : {result.get('erreur', result.get('message'), 'Erreur inconnue')}")

# ❌❌ Bouton pour clôturer toutes les positions ouvertes
if positions and st.button("❌ Clôturer toutes les positions ouvertes"):
    clotures = []
    for p in positions:
        result = cloturer_ordre(p.symbol)
        clotures.append((p.symbol, result))
    st.write("### Résultats des clôtures :")
    for symb, res in clotures:
        if res["statut"] == "ok":
            st.success(f"{symb} : +{res['profit']:.2f} $")
        else:
            st.error(f"{symb} : Erreur - {res.get('erreur', res.get('message'))}")

# 🔁 Fermeture propre de MT5
if MT5_OK:
    mt5.shutdown()
