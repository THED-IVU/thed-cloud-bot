#!/bin/bash
# === Script de test manuel pour guardian_scheduler ===
echo "🔄 Lancement de la planification Guardian IA..."
cd "$(dirname "$0")/guardian"
python3 guardian_scheduler.py
