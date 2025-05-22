import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from handlers import router
from scheduler import scheduler
from database import Database
from config import LOG_CONFIG

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Проверка переменных
if not BOT_TOKEN or not ADMIN_ID:
    raise ValueError("❌ BOT_TOKEN и ADMIN_ID обязательны в .env!")

try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    raise ValueError("❌ ADMIN_ID должен быть числом!")

# Настройка логирования
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Подключаем роутер
    dp.include_router(router)
    
    # Инициализация БД
    Database()._create_tables()
    
    # Запуск планировщика
    await scheduler.start(bot)
    
    # Уведомление админа
    await bot.send_message(ADMIN_ID, "✅ Бот запущен!")
    
    # Запуск поллинга
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
