# package_render_ws.py – Préparation de l’archive pour Render.com

import os
import shutil
import zipfile
import time

# === Étape 1 : Créer le dossier de déploiement
DEPLOY_FOLDER = "render_ws_deploy"
if os.path.exists(DEPLOY_FOLDER):
    shutil.rmtree(DEPLOY_FOLDER)
os.makedirs(DEPLOY_FOLDER)

# === Étape 2 : Fichiers à inclure dans le zip pour Render
fichiers = ["render_launcher.py", "requirements.txt"]
for fichier in fichiers:
    if os.path.exists(fichier):
        shutil.copy(fichier, os.path.join(DEPLOY_FOLDER, fichier))
    else:
        print(f"⚠️ Fichier manquant : {fichier}")

# === Étape 3 : Créer ou écraser requirements.txt
req_path = os.path.join(DEPLOY_FOLDER, "requirements.txt")
with open(req_path, "w") as f:
    f.write("websockets\nrequests\ndotenv\n")

# === Étape 4 : Fichier de config render.yaml
render_yaml = """\
services:
  - type: web
    name: tib-ia-ws-server
    env: python
    buildCommand: ""
    startCommand: python render_launcher.py
    autoDeploy: true
    branch: main
    plan: free
"""
with open(os.path.join(DEPLOY_FOLDER, "render.yaml"), "w") as f:
    f.write(render_yaml)

# === Étape 5 : Injecter automatiquement le code du WebSocket dans render_launcher.py
render_ws_code = '''
# render_launcher.py – WebSocket IA Render avec moteur local

import asyncio
import websockets
import json
import os
from dotenv import load_dotenv
import requests

# Charger les variables d’environnement depuis le .env
load_dotenv()

API_LOCAL_URL = os.getenv("LOCAL_IA_URL", "http://localhost:5000/analyse")
API_KEY = os.getenv("IA_KEY", "demo-key")

print(f"🌐 API IA connectée à : {API_LOCAL_URL}")

async def traiter_signal_brut(donnees):
    try:
        response = requests.post(API_LOCAL_URL, json=donnees, headers={"x-api-key": API_KEY})
        if response.status_code == 200:
            return response.json()
        else:
            return {"erreur": f"⚠️ Erreur IA: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"erreur": f"❌ Exception IA: {str(e)}"}

async def handler(websocket, path):
    print("🔌 Connexion client WebSocket acceptée")
    async for message in websocket:
        try:
            print(f"📥 Message reçu : {message}")
            payload = json.loads(message)

            if payload.get("type") == "SIGNAL_MANUEL_VALIDÉ":
                analyse_ia = await traiter_signal_brut(payload["payload"])
                await websocket.send(json.dumps({"type": "RETOUR_ANALYSE", "data": analyse_ia}))
                print("📤 Résultat IA renvoyé.")
            else:
                await websocket.send(json.dumps({"erreur": "Type inconnu"}))
        except Exception as e:
            print(f"💥 Erreur WebSocket : {e}")
            await websocket.send(json.dumps({"erreur": str(e)}))

start_server = websockets.serve(handler, "0.0.0.0", 8765)

print("🚀 Serveur WebSocket IA prêt sur ws://0.0.0.0:8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
'''

with open(os.path.join(DEPLOY_FOLDER, "render_launcher.py"), "w", encoding="utf-8") as f:
    f.write(render_ws_code.strip())

# === Étape 6 : Création de l'archive .zip
archive_path = "render_ws_secure.zip"
with zipfile.ZipFile(archive_path, "w") as archive:
    for root, dirs, files in os.walk(DEPLOY_FOLDER):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, DEPLOY_FOLDER)
            archive.write(full_path, arcname)

print("✅ Archive prête pour Render :", archive_path)
print("👉 Étapes suivantes :")
print("1. Connecte-toi à https://dashboard.render.com/")
print("2. Crée un nouveau service web à partir d’un dépôt GitHub contenant ce zip.")
print("3. Utilise le fichier render.yaml généré pour la configuration automatique.")
