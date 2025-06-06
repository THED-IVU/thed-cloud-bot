import requests

def get_crypto_sentiment():
    try:
        r = requests.get("https://api.alternative.me/fng/")
        data = r.json()
        return data["data"][0]
    except:
        return {"value": "50", "value_classification": "Neutral"}