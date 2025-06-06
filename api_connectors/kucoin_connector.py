
import requests

def get_kucoin_markets():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Échec de connexion à KuCoin"}
