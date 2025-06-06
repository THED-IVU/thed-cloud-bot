@echo off
title 🚀 Lancement Bot IA THED

cd /d "D:\DOCUMENTATION\PROFESSIONNEL\2025\MES PRODUITS 2025 A VENDRE\TRADING THED\BOT_MT5_THED_PRO_FINAL_CORRECTED\THED"

echo [1/4] Lancement de l'API Flask...
start cmd /k python websocket\api_flask_trade.py

ping 127.0.0.1 -n 5 >nul

echo [2/4] Lancement du simulateur de signaux IA...
start cmd /k python websocket\ws_trade_sender.py

ping 127.0.0.1 -n 3 >nul

echo [3/4] Vérification de l'état de l'API...
python check_flask.py

echo [4/4] Ouverture de l'interface /last_trade dans le navigateur...
start http://127.0.0.1:8000/last_trade

echo ✅ Tous les modules sont lancés.
pause
exit
