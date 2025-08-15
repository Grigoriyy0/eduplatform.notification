from aiogram import Bot

from decouple import config

bot = Bot(config('TOKEN'))
chat_id = config('CHAT_ID')

async def send_notification(notification : str):
    await bot.send_message(chat_id=chat_id, text=notification)