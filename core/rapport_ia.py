import requests
import pandas as pd
from datetime import datetime, timedelta

FIREBASE_URL = "https://thed-ivu-bot-default-rtdb.firebaseio.com"
LOGS_ENDPOINT = f"{FIREBASE_URL}/logs.json"

def charger_logs_firebase():
    try:
        res = requests.get(LOGS_ENDPOINT, timeout=10)
        if res.status_code == 200 and res.json():
            raw_logs = res.json()
            df_logs = pd.DataFrame(list(raw_logs.values()))
            df_logs["datetime"] = pd.to_datetime(df_logs["datetime"])
            return df_logs.sort_values("datetime", ascending=False)
    except:
        pass
    return pd.DataFrame()

def generer_rapport_ia(periode="jour"):
    df = charger_logs_firebase()
    if df.empty:
        return "Aucune donnée IA disponible pour générer un rapport."

    maintenant = datetime.utcnow()
    if periode == "jour":
        df = df[df["datetime"].dt.date == maintenant.date()]
    elif periode == "semaine":
        semaine = maintenant - timedelta(days=7)
        df = df[df["datetime"] > semaine]

    if df.empty:
        return f"Aucun log IA enregistré sur la période sélectionnée ({periode})."

    total = len(df)
    gagnés = len(df[df["resultat"] == "gagné"])
    perdus = len(df[df["resultat"] == "perdu"])
    neutres = len(df[df["resultat"] == "neutre"])
    taux_reussite = round((gagnés / total) * 100, 2) if total > 0 else 0
    score_moyen = round(df["score_ia"].dropna().mean(), 2) if "score_ia" in df else "N/A"

    strategies = df["strategie"].value_counts().to_dict()
    top_strategie = max(strategies, key=strategies.get) if strategies else "Aucune"

    rapport = f"""
📅 Période : {periode.upper()}
📊 Total de signaux IA : {total}
✅ Gagnés : {gagnés}
❌ Perdus : {perdus}
➖ Neutres : {neutres}
🎯 Taux de réussite : {taux_reussite}%
🧠 Score IA moyen : {score_moyen}
🏆 Stratégie la plus utilisée : {top_strategie}
"""

    return rapport.strip()