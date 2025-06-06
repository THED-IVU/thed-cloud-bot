import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

from core.strategie_ema_rsi import detecter_opportunite as strat_ema
from core.strategie_breakout_news import detecter_opportunite as strat_breakout
from core.strategie_heikin_psar import detecter_opportunite as strat_heikin
from core.strategie_fibo_bougies import detecter_opportunite as strat_fibo
from core.strategie_sniper_ia import detecter_opportunite as strat_sniper

from db import inserer_trade  # ✅ IMPORTATION DE LA BASE
STRATEGIES = [
    ("EMA + RSI + MACD", strat_ema),
    ("Breakout + News", strat_breakout),
    ("Heikin Ashi + PSAR", strat_heikin),
    ("Fibonacci + Bougies", strat_fibo),
    ("Sniper IA", strat_sniper)
]

st.set_page_config(page_title="Simulation rapide multi-actifs", layout="wide")
st.title("🔎 Scanner multi-actifs + IA + Heatmap")

# -- Paramètres utilisateur --
st.sidebar.header("⚙️ Paramètres")
actifs = st.sidebar.text_input("Liste d’actifs (séparés par ,)", value="EURUSD=X,GBPUSD=X,USDJPY=X").split(",")
use_ai = st.sidebar.checkbox("🧠 Activer l’IA", value=True)
score_min = st.sidebar.slider("🎯 Score minimum à afficher", 0, 100, 70)
timeframes = ["1h", "15m", "5m"]
periods = {"1h": "3d", "15m": "3d", "5m": "2d"}

# -- Lancer le scan --
if st.button("🚀 Lancer l’analyse complète"):
    tous_les_resultats = []

    for actif in [a.strip().upper() for a in actifs]:
        st.markdown(f"### 📈 Résultats pour `{actif}`")
        global_df = []

        for tf in timeframes:
            lignes = []
            now = datetime.now()

            for nom, strategie in STRATEGIES:
                try:
                    res = strategie(actif, interval=tf, period=periods[tf], use_ai=use_ai)
                    if res and res["score"] >= score_min:
                        lignes.append({
                            
                            "datetime": now.isoformat(),
                            "action": res["decision"].upper(),
                            "price": res.get("entry", 0),
                            "exit_price": res.get("tp", 0),
                            "profit": round(res.get("tp", 0) - res.get("entry", 0), 5) if res["decision"].lower() == "buy" else round(res.get("entry", 0) - res.get("tp", 0), 5),
                            "RSI": res.get("rsi", 0),
                            "MACD": res.get("macd", 0),
                            "MACDs": res.get("macds", 0),
                            "EMA9": res.get("ema9", 0),
                            "EMA21": res.get("ema21", 0),
                            "source": nom,
                            "context": res.get("context", "-"),
                            "note": res.get("score", 0),
                            "score_ia": res.get("score_ia", "-"),
                            "validation_ia": res.get("validation_ia", "-"),
                            "explication_ia": res.get("explication_ia", "-"),
                            "asset": actif,
                            "capital": 0  # valeur fictive (ou remplace par gestion dynamique)
                         }

                        inserer_trade(ligne)  # ✅ ENVOI VERS SQLITE
                        lignes.append({
                            "actif": actif,
                            "timeframe": tf,
                            "stratégie": nom,
                            "score": res["score"],
                            "décision": res["decision"].upper(),
                            "score_ia": res.get("score_ia", "-"),
                            "validation_ia": res.get("validation_ia", "-"),
                            "explication": res.get("context", "-"),
                            "explication_ia": res.get("explication_ia", "-"),
                            "datetime": now.strftime("%Y-%m-%d %H:%M")
                        })
                except Exception as e:
                    lignes.append({
                        "actif": actif, "timeframe": tf, "stratégie": nom, "score": 0,
                        "décision": "Erreur", "score_ia": "-", "validation_ia": "-",
                        "explication": str(e), "explication_ia": "-", "datetime": now.strftime("%Y-%m-%d %H:%M")
                    })

            df = pd.DataFrame(lignes)
            global_df.append(df)

        df_concat = pd.concat(global_df)
        tous_les_resultats.append(df_concat)

        st.dataframe(df_concat, use_container_width=True)

        # 🔥 Heatmap score
        pivot = df_concat.pivot_table(index="stratégie", columns="timeframe", values="score", aggfunc="max")
        st.markdown("#### 🌡️ Heatmap des scores")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.heatmap(pivot, annot=True, fmt=".0f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        # 🧠 Interprétation
        for tf in timeframes:
            df_tf = df_concat[df_concat["timeframe"] == tf]
            if not df_tf.empty:
                df_buy = df_tf[df_tf["décision"] == "BUY"]
                df_sell = df_tf[df_tf["décision"] == "SELL"]
                msg = f"🔍 **{tf.upper()}** : {len(df_buy)} stratégies haussières / {len(df_sell)} baissières"
                st.info(msg)

    # 🔁 Fusion complète
    df_total = pd.concat(tous_les_resultats)
    st.markdown("---")
    st.markdown("## 📊 Résumé global multi-actifs")
    st.dataframe(df_total.sort_values(["actif", "score"], ascending=[True, False]), use_container_width=True)

    # 📤 Export CSV
    csv = df_total.to_csv(index=False).encode("utf-8")
    st.download_button("💾 Télécharger résultats CSV", data=csv, file_name="scanner_resultats.csv", mime="text/csv")

else:
    st.info("Saisis les actifs puis clique sur 🚀 pour lancer l’analyse.")
