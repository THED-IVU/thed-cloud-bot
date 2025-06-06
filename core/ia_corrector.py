import requests
import pandas as pd
from collections import Counter

FIREBASE_URL = "https://thed-ivu-bot-default-rtdb.firebaseio.com/failures.json"

def charger_erreurs():
    try:
        res = requests.get(FIREBASE_URL, timeout=10)
        if res.status_code == 200 and res.json():
            return pd.DataFrame(res.json().values())
    except Exception as e:
        print("Erreur chargement Firebase :", e)
    return pd.DataFrame()

def analyser_erreurs(df):
    print("\n📊 Analyse des erreurs IA :")

    if df.empty:
        print("Aucune erreur enregistrée.")
        return

    # Motifs fréquents par symbole
    symboles = Counter(df["symbole"])
    raisons = Counter(df["raison"])

    print("\n🔠 Symboles les plus concernés :")
    for sym, count in symboles.most_common(5):
        print(f" - {sym} : {count} erreurs")

    print("\n📋 Raisons fréquentes d’échec :")
    for r, count in raisons.most_common(5):
        print(f" - {r} : {count} fois")

    # Recommandations stratégiques
    print("\n🧠 Recommandations IA :")
    for r in raisons:
        if "timeout" in r.lower():
            print("⚠️ Conseil : Allonger le délai d’attente des réponses IA.")
        elif "confiance faible" in r.lower():
            print("📉 Conseil : Réhausser le seuil de confiance IA (ex: passer de 60% à 70%).")
        elif "aucun signal" in r.lower():
            print("🔍 Conseil : Ajouter un fallback ou vérifier les filtres techniques trop stricts.")

    print("\n✅ Fin de l’analyse IA auto-corrective.")

def lancer_correction():
    df = charger_erreurs()
    analyser_erreurs(df)

# Exemple d'exécution manuelle
if __name__ == "__main__":
    lancer_correction()