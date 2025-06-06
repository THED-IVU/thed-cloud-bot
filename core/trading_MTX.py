
from firebase_logger import envoyer_log_firebase

def executer_trade(symbole, direction, strategie="IA_AUTO", resultat="en attente", volume=1.0, expiration=60):
    """
    Simule l’exécution d’un trade et journalise l'action. À connecter à MT5 si nécessaire.
    """
    print(f"📤 Exécution trade : {symbole} | {direction} | Vol: {volume} | Exp: {expiration}s")

    envoyer_log_firebase(
        symbole=symbole,
        action=direction,
        resultat=resultat,
        strategie=strategie
    )

    return {"statut": "envoyé", "symbole": symbole, "volume": volume, "expiration": expiration}
