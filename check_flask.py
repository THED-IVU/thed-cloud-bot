import requests

def test_flask_connection():
    try:
        url = "http://localhost:8000/last_trade"
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ Flask API est bien active sur localhost:8000")
            print("Contenu de /last_trade :", response.json())
        else:
            print("❌ Réponse inattendue :", response.status_code)
    except Exception as e:
        print("❌ Erreur de connexion à l’API Flask :", e)

if __name__ == "__main__":
    test_flask_connection()
