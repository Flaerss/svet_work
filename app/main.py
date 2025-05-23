import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Локальные импорты
from app.handlers import client_handlers
from app.services.yclients_service import YClientsAPI
from app.database import get_async_db, init_db
from config import Config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=Config.LOGS_DIR / "bot.log"
)
logger = logging.getLogger(__name__)

async def main():
    """Точка входа для Telegram-бота"""
    
    # 1. Инициализация
    load_dotenv()
    Config.create_dirs()
    init_db()  # Создание таблиц если их нет
    
    # 2. Создаем экземпляры бота и диспетчера
    bot = Bot(token=Config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # 3. Регистрируем обработчики
    dp.include_router(client_handlers.router)
    
    # 4. Инициализация сервисов
    yclients = YClientsAPI()
    scheduler = AsyncIOScheduler()
    
    # 5. Настройка планировщика
    @scheduler.scheduled_job("interval", minutes=30)
    async def check_reminders():
        async with get_async_db() as db:
            # Логика проверки напоминаний
            pass
            
    scheduler.start()
    
    # 6. Уведомление о запуске
    await bot.send_message(
        chat_id=Config.ADMIN_ID,
        text="🤖 Бот успешно запущен!"
    )
    
    # 7. Запуск поллинга
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен вручную")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {str(e)}")