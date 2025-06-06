@echo off
title 🚀 THED IVU BOT - Lancement automatique
echo Lancement de l'API Flask (localhost:8000)...
start cmd /k "cd websocket && python api_flask_trade.py"
timeout /t 2 > nul
echo Lancement du simulateur IA vers API Flask...
start cmd /k "cd websocket && python ws_trade_sender.py"
