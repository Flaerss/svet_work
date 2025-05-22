from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import logging

logger = logging.getLogger(__name__)

async def start_handler(message: types.Message) -> None:
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение и регистрирует пользователя.
    """
    try:
        user = message.from_user
        logger.info(f"Новый пользователь: {user.full_name} (ID: {user.id})")
        await message.answer(
            "Привет! Я бот Фотостудии SVET 📸\n\n"
            "Чем могу помочь?\n"
            "Доступные команды:\n"
            "/booking - Записаться на сессию\n"
            "/help - Помощь"
        )
    except Exception as e:
        logger.error(f"Ошибка в start_handler: {e}", exc_info=True)

async def help_handler(message: types.Message) -> None:
    """Обработчик команды /help"""
    help_text = (
        "🤖 Список доступных команд:\n\n"
        "/start - Перезапустить бота\n"
        "/booking - Записаться на фотосессию\n"
        "/cancel - Отменить текущее действие\n"
        "/my_bookings - Просмотреть ваши записи"
    )
    await message.answer(help_text)

def register_handlers(dp: Dispatcher) -> None:
    """
    Регистрация всех обработчиков команд
    
    Args:
        dp (Dispatcher): Диспетчер Aiogram
    """
    dp.register_message_handler(start_handler, commands=["start"], state="*")
    dp.register_message_handler(help_handler, commands=["help"], state="*")
    logger.info("Обработчики команд успешно зарегистрированы")
