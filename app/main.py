import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv
from app.handlers import client_handlers

load_dotenv()

async def main():
    try:
        bot = Bot(token=os.getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
        dp = Dispatcher()
        dp.include_router(client_handlers.router)

        async with bot.context():
            await dp.start_polling(bot)

    except TokenValidationError:
        print("⚠️ Неверный токен бота!")
    except Exception as e:
        print(f"🚨 Критическая ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
