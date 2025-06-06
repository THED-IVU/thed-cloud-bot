from datetime import datetime

def is_news_period():
    now = datetime.utcnow()
    minute = now.minute
    if minute in range(25, 35):  # Simule 5 min avant/après
        return True
    return False