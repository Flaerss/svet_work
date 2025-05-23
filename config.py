import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

async def main():
    try:
        bot = Bot(token=Config.BOT_TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher()
        
        # Импорт обработчиков
        from app.handlers import router
        dp.include_router(router)
        
        # Запуск
        logging.info("Бот запущен")
        await dp.start_polling(bot)
        
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    finally:
        logging.info("Бот остановлен")

if __name__ == "__main__":
    asyncio.run(main())
