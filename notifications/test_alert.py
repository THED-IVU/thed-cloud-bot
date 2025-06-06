from notifications.telegram_alert import envoyer_alerte_telegram

# 🔁 Exemple de trade simulé pour test complet
test_msg = {
    "symbol": "EURUSD",
    "direction": "📈 UP",
    "confiance": 89,
    "mise": 10,
    "duree": 30,
    "contexte": "Range haussier confirmé sur M15 et M5",
    "resume_technique": "✅ RSI=75 (surachat)\n✅ EMA 9 > EMA 21\n✅ MACD positif",
    "resume_fondamentale": "📉 USD stable malgré les tensions sur la BCE\n📰 Pas de news majeures aujourd’hui"
}

# 🟢 Test d’envoi Telegram avec message contextuel
envoyer_alerte_telegram(test_msg, "🟢 Trade TEST IA – Analyse complète envoyée")
