
# MON_API_PRO/web_crawler_fondamental.py

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le .env du projet global
load_dotenv(dotenv_path=os.path.join("D:/DOCUMENTATION/PROFESSIONNEL/2025/MES PRODUITS 2025 A VENDRE/TRADING THED/BOT_MT5_THED_PRO_FINAL_CORRECTED/THED", ".env"))

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "demo_news_api_key")

def recuperer_actualites_economiques(pays="us", mots_cles="federal reserve", max_articles=5):
    resultats = []
    try:
        url = f"https://newsapi.org/v2/everything?q={mots_cles}&language=en&pageSize={max_articles}"
        headers = {
            "Authorization": NEWS_API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for article in data.get("articles", [])[:max_articles]:
                resultats.append({
                    "titre": article["title"],
                    "source": article["source"]["name"],
                    "url": article["url"],
                    "date": article["publishedAt"]
                })
        else:
            resultats.append({"erreur": f"Code {response.status_code} – {response.text}"})
    except Exception as e:
        resultats.append({"erreur": str(e)})

    return {
        "horodatage": datetime.now().isoformat(),
        "pays": pays,
        "mots_cles": mots_cles,
        "actualites": resultats
    }

if __name__ == "__main__":
    print(recuperer_actualites_economiques())
