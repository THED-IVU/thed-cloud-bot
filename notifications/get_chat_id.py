import asyncio
from telegram import Bot

BOT_TOKEN = "7523104198:AAHcx-4NMKI00qggdCXOOff0DhLn5TJDTvg"

async def main():
    bot = Bot(token=BOT_TOKEN)
    updates = await bot.get_updates()
    if not updates:
        print("❌ Aucun message détecté. Envoie un message dans le groupe.")
        return
    for update in updates:
        try:
            chat_id = update.message.chat.id
            chat_name = update.message.chat.title
            print(f"✅ Chat ID détecté : {chat_id} - Nom du groupe : {chat_name}")
        except Exception as e:
            print(f"Erreur : {e}")

if __name__ == "__main__":
    asyncio.run(main())
