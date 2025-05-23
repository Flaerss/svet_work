import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.utils.token import TokenValidationError
from dotenv import load_dotenv

# Относительный импорт для Render
from .handlers import client_handlers  # Изменено с app.handlers

# Настройка логирования в файл
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log',  # Логи будут сохраняться в файл
    filemode='a'         # Режим добавления логов
)

load_dotenv()

async def main():
    try:
        # Проверка токена
        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token:
            raise ValueError("❌ BOT_TOKEN не найден в .env")
            
        # Инициализация бота
        bot = Bot(token=bot_token, parse_mode=ParseMode.HTML)
        dp = Dispatcher()
        
        # Регистрация роутера
        dp.include_router(client_handlers.router)
        
        # Уведомление о запуске
        logging.info("=== Бот запущен ===")
        print("✅ Бот успешно инициализирован")
        
        # Запуск поллинга
        await dp.start_polling(bot)

    except TokenValidationError:
        logging.critical("⚠️ Невалидный токен бота!")
    except Exception as e:
        logging.error(f"🚨 Ошибка: {str(e)}", exc_info=True)
    finally:
        logging.info("=== Бот остановлен ===")
        await bot.close() if 'bot' in locals() else None

if __name__ == "__main__":
    asyncio.run(main())
