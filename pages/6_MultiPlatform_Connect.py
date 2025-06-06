
import streamlit as st

st.set_page_config(page_title="Multi-Plateforme - THED IVU BOT", layout="wide")
st.title("🌐 Connexion Multi-Plateforme")

st.markdown("""
### Sélectionnez une plateforme de trading externe :

- 🔵 [Pocket Option](https://pocketoption.com/fr/)
- 🟡 [Binance](https://www.binance.com/)
- 🔴 [KuCoin](https://www.kucoin.com/)
- 🟣 [TradingView](https://www.tradingview.com/)

---

### Options de configuration
""")

platform = st.selectbox("📍 Plateforme cible", ["Pocket Option", "Binance", "KuCoin", "TradingView"])

if platform == "Pocket Option":
    st.success("📈 Connectez-vous manuellement à Pocket Option via le navigateur.")
    st.markdown("[Accéder à Pocket Option](https://pocketoption.com/fr/)", unsafe_allow_html=True)

elif platform == "Binance":
    st.info("🛠️ Une API clé et un secret sont requis pour Binance.")
    api_key = st.text_input("🔑 Clé API Binance")
    api_secret = st.text_input("🕵️ Secret API Binance", type="password")
    if api_key and api_secret:
        st.success("✅ Clé API reçue. Module Binance prêt à configurer.")

elif platform == "KuCoin":
    st.warning("⚠️ Module KuCoin encore en cours de développement.")
    st.markdown("Consultez [KuCoin API](https://www.kucoin.com/docs) pour les détails.")

elif platform == "TradingView":
    st.info("🔗 Utilisez les Webhooks TradingView pour envoyer vos signaux ici.")
    st.markdown("Endpoint : `http://<votre_ip>:<port>/webhook`")
    st.code('{ "ticker": "EURUSD", "signal": "buy", "timeframe": "1m" }', language="json")

st.markdown("---")
st.caption("© 2025 - THED IVU BOT | Interface multi-plateforme")
