
import os
import json
from datetime import datetime
import streamlit as st
import pandas as pd
import requests

from db import lire_trades

try:
    from runtime_config import get_runtime_config
except ImportError:
    def get_runtime_config():
        return {
            "use_ai": True,
            "default_action": "HOLD",
            "default_score": "5.0/10",
            "ai_provider": "openai",
            "openai": {"api_key": os.getenv("OPENAI_API_KEY"), "model": "gpt-3.5-turbo"},
            "gemini": {"api_key": "", "model": "gemini-pro"},
            "claude": {"api_key": "", "model": "claude-3-sonnet-20240229"},
            "mistral": {"api_key": "", "model": "mistral-small"},
            "groq": {"api_key": "", "model": "mixtral-8x7b-32768"},
            "openrouter": {"api_key": "", "model": "mistralai/mistral-7b-instruct"}
        }

IA_DECISION_LOG = "historique_decisions_ia.json"

def construire_prompt(dataframe: pd.DataFrame) -> str:
    dataframe.columns = dataframe.columns.str.lower()
    colonnes_voulues = ['close', 'rsi', 'macd_12_26_9', 'macds_12_26_9', 'ema9', 'ema21', 'signal']
    colonnes_existantes = [col for col in colonnes_voulues if col in dataframe.columns]
    colonnes_manquantes = [col for col in colonnes_voulues if col not in dataframe.columns]

    if not colonnes_existantes:
        return "Données techniques insuffisantes pour analyser cette configuration."

    dernieres_lignes = dataframe.tail(5).to_dict(orient="records")
    resume = " | ".join(col.upper() for col in colonnes_existantes) + "\n"
    for ligne in dernieres_lignes:
        resume += " | ".join(str(ligne.get(col, "-")) for col in colonnes_existantes) + "\n"

    prompt = "Données techniques récentes pour l'actif analysé :\n"
    prompt += resume + "\n"
    if colonnes_manquantes:
        prompt += "Colonnes manquantes (non bloquantes) : " + ", ".join(colonnes_manquantes) + "\n"

    prompt += (
        "Tu es un expert en scalping Forex & crypto.\n"
        "Analyse les données ci-dessus et fournis une recommandation de trade rapide (1-5min) dans ce format :\n\n"
        "TREND: (uptrend/downtrend/neutral)\n"
        "ACTION: (BUY/SELL/HOLD)\n"
        "RISK: (brève évaluation du risque)\n"
        "SCORE: (note sur 10 de la fiabilité)\n"
        "CONTEXT: (type d’opportunité)\n"
        "JUSTIFICATION: (analyse technique + intuition IA résumée)"
    )
    return prompt

def _analyse_openai(prompt: str, config: dict) -> str:
    try:
        from openai import OpenAI
        api_key = config["openai"].get("api_key") or os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "[ERREUR OpenAI] Clé API manquante."
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=config["openai"].get("model", "gpt-3.5-turbo"),
            messages=[
                {"role": "system", "content": "Tu es un expert en trading IA spécialisé en scalping."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERREUR OpenAI] {e}"

fournisseurs_ia = {
    "openai": _analyse_openai
}

def parser_resultat_ia(resultat: str) -> dict:
    lignes = resultat.strip().split("\n")
    data = {"TREND": "", "ACTION": "", "RISK": "", "SCORE": "", "CONTEXT": "", "JUSTIFICATION": ""}
    for ligne in lignes:
        if ":" in ligne:
            cle, valeur = ligne.split(":", 1)
            cle = cle.strip().upper()
            valeur = valeur.strip()
            if cle in data:
                data[cle] = valeur
    return data

def analyser_avec_ia(summary_df: pd.DataFrame) -> dict:
    CONFIG = get_runtime_config()
    if not CONFIG["use_ai"]:
        return {
            "TREND": "neutral",
            "ACTION": CONFIG["default_action"],
            "RISK": "IA désactivée (mode technique only)",
            "SCORE": CONFIG["default_score"],
            "CONTEXT": "technical only",
            "JUSTIFICATION": "Aucune analyse IA car le mode IA est désactivé."
        }

    prompt = construire_prompt(summary_df)
    fournisseur = CONFIG.get("ai_provider", "openai").lower()
    analyse_brute = fournisseurs_ia.get(fournisseur, _analyse_openai)(prompt, CONFIG)
    analyse = parser_resultat_ia(analyse_brute)
    analyse = ponderer_par_performance(analyse)
    enregistrer_decision_ia(analyse)
    return analyse

def enregistrer_decision_ia(analyse_dict: dict):
    try:
        historique = []
        if os.path.exists(IA_DECISION_LOG):
            with open(IA_DECISION_LOG, "r") as f:
                historique = json.load(f)
        analyse_dict["timestamp"] = datetime.now().isoformat()
        historique.append(analyse_dict)
        with open(IA_DECISION_LOG, "w") as f:
            json.dump(historique, f, indent=2)
    except Exception as e:
        st.warning(f"Erreur lors de l'enregistrement de la décision IA : {e}")

def ponderer_par_performance(analyse: dict) -> dict:
    try:
        score_str = analyse.get("SCORE", "5.0").split("/")[0]
        score = float(score_str) if score_str.strip() else 5.0

        if not isinstance(score, (int, float)) or pd.isna(score):
            score = 2.0

        action = analyse.get("ACTION", "HOLD").upper()
        df = lire_trades()
        if df.empty or "action" not in df:
            analyse["SCORE"] = f"{score:.1f}/10"
            return analyse

        recent = df.tail(20)
        buy_perf = recent[recent["action"] == "BUY"]["profit"].mean()
        sell_perf = recent[recent["action"] == "SELL"]["profit"].mean()

        if action == "BUY" and buy_perf < 0:
            score -= 1
        elif action == "SELL" and sell_perf < 0:
            score -= 1
        elif action in ["BUY", "SELL"] and (buy_perf > 0 or sell_perf > 0):
            score += 0.5

        score = max(0, min(10, score))
        analyse["SCORE"] = f"{score:.1f}/10"
        return analyse

    except Exception as e:
        st.warning(f"⚠️ Erreur de pondération IA : {e}")
        analyse["SCORE"] = "5.0/10"
        return analyse
