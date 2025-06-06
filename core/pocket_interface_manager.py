# pocket_interface_manager.py – Configuration multi-fenêtres Pocket Option

FENETRES_CONFIG = {
    1: {"symbol": "EURUSD", "window_id": "F1"},
    2: {"symbol": "BTCUSD", "window_id": "F2"},
    3: {"symbol": "ETHUSD", "window_id": "F3"},
    4: {"symbol": "USDJPY", "window_id": "F4"}
}

def get_config_par_fenetre(numero):
    """
    Retourne la configuration associée à une fenêtre spécifique (1 à 4).
    """
    return FENETRES_CONFIG.get(numero, {})
