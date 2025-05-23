import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv

load_dotenv()

async def main():
    try:
        bot = Bot(
            token=os.getenv("BOT_TOKEN"),
            parse_mode=ParseMode.HTML
        )
        dp = Dispatcher()
        
        # Регистрация обработчиков
        from .handlers import client_handlers
        dp.include_router(client_handlers.router)
        
        await dp.start_polling(bot)
        
    except TokenValidationError:
        logging.error("⚠️ Неверный токен бота!")
    except Exception as e:
        logging.error(f"🚨 Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
