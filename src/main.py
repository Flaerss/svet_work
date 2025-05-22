import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from handlers import register_handlers
from scheduler import scheduler
from database import Database
from config import LOG_CONFIG, DATA_DIR

# Загрузка конфигурации
logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_URL = "https://your-service.onrender.com/webhook"
PORT = int(os.getenv("PORT", 8000))

async def on_startup(app: web.Application):
    Database()._create_tables()  # Инициализация БД
    await scheduler.start(Bot(token=BOT_TOKEN))
    await Bot(token=BOT_TOKEN).send_message(ADMIN_ID, "✅ Бот запущен!")

if __name__ == "__main__":
    app = web.Application()
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    register_handlers(dp)
    setup_application(app, dp, bot=bot)
    app.on_startup.append(on_startup)
    web.run_app(app, host="0.0.0.0", port=PORT)
