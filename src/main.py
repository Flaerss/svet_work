import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from handlers import register_handlers
from scheduler import scheduler
from database import Database
from config import LOG_CONFIG

# Настройка логирования
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_URL = "https://your-service.onrender.com/webhook"
PORT = int(os.getenv("PORT", 8000))

async def on_startup(app: web.Application):
    """Действия при запуске"""
    Database()._create_tables()
    await scheduler.start(Bot(token=BOT_TOKEN))
    await Bot(token=BOT_TOKEN).send_message(ADMIN_ID, "✅ Бот запущен!")

if __name__ == "__main__":
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    register_handlers(dp)
    
    app = web.Application()
    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    web.run_app(app, host="0.0.0.0", port=PORT)
