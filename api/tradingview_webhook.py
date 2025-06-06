
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("🔔 Signal reçu de TradingView :", data)
    # À améliorer : validation + sauvegarde + déclencheur bot
    return jsonify({"status": "ok", "received": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
