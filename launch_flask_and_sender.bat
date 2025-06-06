@echo off
title Lancement API Flask et Sender THED
cd /d "%~dp0"
start "API Flask" cmd /k "python api_flask_trade.py"
timeout /t 3 /nobreak >nul
start "Sender WS" cmd /k "python ws_trade_sender.py"
