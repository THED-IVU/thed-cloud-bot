
@echo off
echo 🚀 Lancement de Guardian IA (Réorganisation + Sync + Scheduler)...

:: Lancer la réorganisation immédiate
python guardian\guardian_organizer.py

:: Lancer la synchronisation
python guardian\guardian_sync.py

:: Lancer le scheduler principal (corrections automatiques toutes les heures)
start python guardian\guardian_scheduler.py

:: Lancer le scheduler secondaire (maj complète toutes les 6 heures)
start python guardian\guardian_updater.py

echo ✅ Tous les processus Guardian sont lancés.
pause
