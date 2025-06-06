@echo off
echo 🚀 Lancement du Copilote IA Pocket Option
cd /d %~dp0
start "" http://localhost:8502
start cmd /k "streamlit run pages\6_PocketOption_Copilote_FINAL.py --server.port 8502"
start cmd /k "ngrok http 8502"
