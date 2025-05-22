import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import setup_application
from aiohttp import web
from handlers import register_handlers
from scheduler import scheduler

# Загрузка переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_URL = "https://your-service.onrender.com/webhook"  # Замените на ваш URL
PORT = int(os.getenv("PORT", 8000))  # Порт для Render

# Инициализация
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()
register_handlers(dp)  # Регистрация обработчиков

async def on_startup(app: web.Application):
    await bot.set_webhook(WEBHOOK_URL)
    await scheduler.start(bot)  # Запуск планировщика
    await bot.send_message(ADMIN_ID, "✅ Бот запущен!")

async def on_shutdown(app: web.Application):
    await bot.session.close()
    await scheduler.shutdown()

if __name__ == "__main__":
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=PORT)
