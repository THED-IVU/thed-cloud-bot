import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Configuration
TOKEN = "7523104198:AAHcx-4NMKI00qggdCXOOff0DhLn5TJDTvg"
AUTHORIZED_USER_ID = 675564258  # Modifier si nécessaire

# Configurer le logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Commande de démarrage
def start(update, context):
    update.message.reply_text("🤖 TIB Bot actif. Tape /help pour voir les commandes.")

# Commande d’aide
def help_command(update, context):
    update.message.reply_text("/start - Activer le bot\n/status - Vérifier l'état\n/signal - Recevoir un exemple de signal")

# Statut
def status(update, context):
    update.message.reply_text("✅ Le bot fonctionne correctement.")

# Simuler un envoi de signal
def signal(update, context):
    message = "🚨 Nouveau signal IA 🚨\nActif: EURUSD\nDirection: UP\nScore: 87%\nDurée: 60s"
    update.message.reply_text(message)

# Fonction principale
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("status", status))
    dp.add_handler(CommandHandler("signal", signal))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
