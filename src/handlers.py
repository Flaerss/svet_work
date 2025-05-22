from aiogram.filters import Command
from database import Database  # Добавьте импорт

async def booking_handler(message: types.Message):
    """Обработчик команды /booking"""
    db = Database()
    user = db.get_user(message.from_user.id)
    if not user:
        db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username
        )
    await message.answer("📅 Введите дату фотосессии (например, 2023-12-31 15:00):")

async def my_bookings_handler(message: types.Message):
    """Обработчик команды /my_bookings"""
    db = Database()
    bookings = db.get_upcoming_sessions(user_id=message.from_user.id)
    if bookings:
        text = "Ваши записи:\n" + "\n".join(
            f"📅 {b.session_date.strftime('%d.%m.%Y %H:%M')}" 
            for b in bookings
        )
    else:
        text = "У вас нет активных записей 😔"
    await message.answer(text)

def register_handlers(dp: Dispatcher) -> None:
    # Добавьте новые обработчики
    dp.register_message_handler(booking_handler, Command("booking"), state="*")
    dp.register_message_handler(my_bookings_handler, Command("my_bookings"), state="*")
