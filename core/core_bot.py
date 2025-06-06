# core/core_bot.py – Fonction principale d’exécution du bot

import logging
from ai import analyser_avec_ia, parser_resultat_ia
from indicators import calculer_tous_les_indicateurs
from core.trading_MTX import executer_trade, cloturer_ordre
from core.forex_manager import cloture_auto_si_tp_sl
from core.init_mt5_connection import get_prix_reel  # ⬅️ Nouvelle importation

def run_bot(symbol, use_ai, trade_manager):
    """
    Exécute une décision de trading et retourne la décision + résultat ('gain', 'perte', 'neutre')
    """
    try:
        logging.info(f"📈 Analyse de {symbol} en cours...")

        # 0. Récupération du prix réel via MT5
        prix_actuel = get_prix_reel(symbol)
        if prix_actuel is None:
            logging.warning("⚠️ Prix réel non disponible, annulation du cycle.")
            return "erreur", "neutre"

        # 1. Vérification SL/TP
        messages = cloture_auto_si_tp_sl(symbol, prix_actuel)
        for msg in messages:
            logging.warning(f"📤 {msg}")

        # 2. Récupération des données & indicateurs
        data, signals = calculer_tous_les_indicateurs(symbol)
        logging.debug(f"✅ Données récupérées, signaux détectés : {signals}")

        # 3. Décision IA ou technique
        if use_ai:
            logging.info("🔍 Analyse IA en cours...")
            prompt = f"Voici les signaux techniques pour {symbol} : {signals}. Quelle est ta recommandation ?"
            ia_result = analyser_avec_ia(prompt)
            decision = parser_resultat_ia(ia_result).get("decision", "neutre")
            logging.info(f"🤖 Décision IA : {decision}")
        else:
            decision = signals.get("signal_global", "neutre")
            logging.info(f"📊 Décision technique : {decision}")

        # 4. Passage à l’action
        if decision.lower() in ["achat", "vente"]:
            resultat = executer_trade(symbol, decision.lower(), trade_manager)
            logging.info(f"✅ Trade exécuté : {decision.upper()} | Résultat : {resultat}")
        else:
            resultat = "neutre"
            logging.info("🚫 Aucune condition remplie pour trader.")

        return decision, resultat

    except Exception as e:
        logging.error(f"❌ Erreur dans run_bot : {e}")
        return "erreur", "neutre"
