from aiogram import Bot, Dispatcher
import asyncio
from decouple import config
from services.consumer import create_connection

async def main() -> None:

    bot = Bot(token=config('TOKEN'))
    dp = Dispatcher()

    await create_connection()

    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    asyncio.run(main())