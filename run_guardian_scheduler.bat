@echo off
REM === Script pour lancer la planification Guardian IA ===
echo 🔄 Lancement de la planification Guardian IA...
cd /d %~dp0guardian
python guardian_scheduler.py
pause
