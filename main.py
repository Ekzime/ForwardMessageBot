# main.py

import asyncio
import logging
from aiogram import Dispatcher
# Импортируем Bot и DefaultBotProperties из нужных модулей aiogram 3.x
from aiogram.client.bot import Bot, DefaultBotProperties

import config
from handlers import router

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )

async def main():
    setup_logging()
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()
    dp.include_router(router)
    logging.info("Бот запускается...")
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
