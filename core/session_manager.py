from datetime import datetime

def get_session():
    heure = datetime.utcnow().hour
    if 0 <= heure < 6:
        return "Asie"
    elif 6 <= heure < 12:
        return "Europe"
    elif 12 <= heure < 20:
        return "US"
    else:
        return "Clôture"

def session_active():
    session = get_session()
    jour = datetime.utcnow().weekday()
    if jour == 4 and get_session() == "US":  # Vendredi après-midi
        return False
    if jour == 0 and get_session() == "Europe":  # Lundi matin
        return False
    return True