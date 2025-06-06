#!/bin/bash

# Aller dans le dossier jobs
cd /chemin/vers/BOT_MT5_THED_PRO/jobs

# Lancer tous les cron jobs (en arrière-plan)
nohup python3 telegram_cron.py &
nohup python3 email_cron.py &
nohup python3 pdf_daily_cron.py &
