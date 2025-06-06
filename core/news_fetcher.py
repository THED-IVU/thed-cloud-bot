"""
news_fetcher.py – Récupération sécurisée de l’actualité économique pour analyse fondamentale
"""

import requests
from datetime import datetime, timedelta
import logging

# Configuration
NEWS_API_KEY = "YOUR_NEWSAPI_KEY"  # Remplacer par ta clé réelle
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
DEFAULT_KEYWORDS = ["forex", "crypto", "inflation", "central banks", "interest rates"]
LOG_PATH = "access_logs/news_fetcher.log"

os.makedirs("access_logs", exist_ok=True)

def fetch_news(keywords=DEFAULT_KEYWORDS, from_days_ago=1):
    """Récupère les articles récents liés aux mots-clés fournis."""
    all_articles = []
    from_date = (datetime.now() - timedelta(days=from_days_ago)).strftime("%Y-%m-%d")

    for kw in keywords:
        params = {
            "q": kw,
            "from": from_date,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": NEWS_API_KEY,
            "pageSize": 5
        }
        try:
            response = requests.get(NEWS_ENDPOINT, params=params)
            response.raise_for_status()
            articles = response.json().get("articles", [])
            all_articles.extend(articles)

        except Exception as e:
            logging.warning(f"[{datetime.now().isoformat()}] ❌ Erreur API pour '{kw}': {e}")
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().isoformat()}] ❌ Erreur API pour '{kw}': {e}\n")

    return all_articles

def afficher_news(n=5):
    """Affiche un résumé des dernières actualités financières."""
    news = fetch_news()
    print(f"📰 Dernières actus économiques :")
    for i, article in enumerate(news[:n], 1):
        print(f"📌 {i}. {article['title']}")
        print(f"    🗞️ {article['source']['name']} | {article['publishedAt']}")
        print(f"    🔗 {article['url']}")
        print()

if __name__ == "__main__":
    afficher_news()
