from aiogram import types
from aiogram.filters import Command
from aiogram import Dispatcher
import logging
from database import Database

logger = logging.getLogger(__name__)

async def start_handler(message: types.Message) -> None:
    """Обработчик команды /start"""
    try:
        db = Database()
        user = db.get_user(message.from_user.id)
        if not user:
            db.add_user(
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username
            )
        await message.answer(
            "Привет! Я бот Фотостудии SVET 📸\n\n"
            "Доступные команды:\n"
            "/booking - Записаться\n"
            "/my_bookings - Мои записи\n"
            "/help - Помощь"
        )
    except Exception as e:
        logger.error(f"Ошибка: {e}", exc_info=True)

async def booking_handler(message: types.Message):
    """Обработчик команды /booking"""
    await message.answer("📅 Введите дату фотосессии в формате ГГГГ-ММ-ДД ЧЧ:ММ")

async def my_bookings_handler(message: types.Message):
    """Обработчик команды /my_bookings"""
    db = Database()
    bookings = db.get_upcoming_sessions(message.from_user.id)
    response = "Ваши записи:\n" + "\n".join(
        f"📅 {b.session_date.strftime('%d.%m.%Y %H:%M')}" 
        for b in bookings
    ) if bookings else "❌ У вас нет активных записей"
    await message.answer(response)

def register_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_handler, Command("start"))
    dp.register_message_handler(booking_handler, Command("booking"))
    dp.register_message_handler(my_bookings_handler, Command("my_bookings"))
