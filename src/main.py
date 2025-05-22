import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from dotenv import load_dotenv
from handlers import register_handlers
from scheduler import scheduler
from database import Database
from config import LOG_CONFIG

# Загрузка переменных окружения из .env
load_dotenv()

# Проверка обязательных переменных
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
PORT = os.getenv("PORT", "8000")  # Значение по умолчанию для порта

if not BOT_TOKEN or not ADMIN_ID:
    raise ValueError("❌ BOT_TOKEN и ADMIN_ID должны быть заданы в .env!")

try:
    ADMIN_ID = int(ADMIN_ID)  # Конвертация в число
except ValueError:
    raise ValueError("❌ ADMIN_ID должен быть числом (например: 123456789)!")

# Настройка логирования
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

async def on_startup(app: web.Application):
    """Действия при запуске бота"""
    try:
        # Инициализация базы данных
        Database()._create_tables()
        logger.info("✅ База данных инициализирована")

        # Запуск планировщика
        await scheduler.start(Bot(token=BOT_TOKEN))
        logger.info("✅ Планировщик задач запущен")

        # Уведомление админа
        await Bot(token=BOT_TOKEN).send_message(ADMIN_ID, "🤖 Бот успешно запущен!")
        
    except Exception as e:
        logger.critical(f"❌ Ошибка при запуске: {e}", exc_info=True)
        raise

async def on_shutdown(app: web.Application):
    """Действия при остановке бота"""
    await Bot(token=BOT_TOKEN).session.close()
    logger.info("✅ Ресурсы освобождены")

if __name__ == "__main__":
    try:
        # Инициализация бота и диспетчера
        bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
        dp = Dispatcher()

        # Регистрация обработчиков
        register_handlers(dp)

        # Настройка веб-сервера
        app = web.Application()
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)
        setup_application(app, dp, bot=bot)

        # Запуск приложения
        web.run_app(
            app,
            host="0.0.0.0",
            port=int(PORT),
            print=lambda _: logger.info(f"🚀 Сервер запущен на порту {PORT}")
        )

    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
