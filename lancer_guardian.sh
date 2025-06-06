
#!/bin/bash
echo "🚀 Lancement de Guardian IA (Réorganisation + Sync + Scheduler)..."

# Réorganisation immédiate
python3 guardian/guardian_organizer.py

# Synchronisation initiale
python3 guardian/guardian_sync.py

# Lancement du scheduler principal
nohup python3 guardian/guardian_scheduler.py > logs/scheduler.log 2>&1 &

# Lancement du scheduler secondaire
nohup python3 guardian/guardian_updater.py > logs/updater.log 2>&1 &

echo "✅ Tous les processus Guardian sont lancés."
