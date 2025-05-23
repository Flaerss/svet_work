from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from datetime import datetime

# Локальные импорты
from app.services.yclients_service import YClientsAPI
from app.database import get_async_db
from app.models import Client, Booking
from config import Config

router = Router()
yclients = YClientsAPI()

# -------------------------
# Обработчики команд
# -------------------------

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    """Приветствие и регистрация пользователя"""
    async with get_async_db() as db:
        # Проверяем существующего пользователя
        existing_user = await db.execute(
            select(Client).where(Client.telegram_id == message.from_user.id)
        )
        existing_user = existing_user.scalar_one_or_none()

        if not existing_user:
            # Регистрируем нового клиента
            new_client = Client(
                telegram_id=message.from_user.id,
                phone=None,
                created_at=datetime.utcnow()
            )
            db.add(new_client)
            await db.commit()

    await message.answer(
        "📸 Добро пожаловать в фотостудию SVET!\n\n"
        "👉 Для записи используйте /booking\n"
        "👉 Ваши записи: /my_bookings",
        reply_markup=ReplyKeyboardRemove()
    )

@router.message(Command("booking"))
async def booking_cmd(message: types.Message, state: FSMContext):
    """Начало процесса записи"""
    await message.answer(
        "📅 Введите дату и время фотосессии в формате:\n"
        "<b>ДД.ММ.ГГГГ ЧЧ:MM</b>\n"
        "Например: 25.12.2023 15:30"
    )
    await state.set_state("waiting_date")

@router.message(F.text.regexp(r'\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}'))
async def process_booking_date(message: types.Message, state: FSMContext):
    """Обработка даты от пользователя"""
    try:
        session_date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        
        # Создаем запись через YClients API
        async with get_async_db() as db:
            client = await db.execute(
                select(Client).where(Client.telegram_id == message.from_user.id))
            client = client.scalar_one()

            # Синхронизация с YClients
            yclients_response = await yclients.create_booking(
                client_id=client.id,
                date=session_date
            )

            if yclients_response.get("success"):
                # Сохраняем в локальную БД
                new_booking = Booking(
                    client_id=client.id,
                    session_date=session_date,
                    status="active"
                )
                db.add(new_booking)
                await db.commit()

                await message.answer(
                    "✅ Запись успешно создана!\n"
                    f"Дата: {session_date.strftime('%d.%m.%Y %H:%M')}\n"
                    "Мы напомним вам за день и за час до сессии."
                )
            else:
                await message.answer("❌ Ошибка при создании записи в системе")

    except ValueError:
        await message.answer("⚠️ Неверный формат даты! Попробуйте еще раз")
    finally:
        await state.clear()

@router.message(Command("my_bookings"))
async def my_bookings_cmd(message: types.Message):
    """Показать активные записи пользователя"""
    async with get_async_db() as db:
        bookings = await db.execute(
            select(Booking)
            .where(Booking.client_id == message.from_user.id)
            .where(Booking.status == "active")
        )
        bookings = bookings.scalars().all()

    if bookings:
        response = ["🗓 Ваши активные записи:"]
        for booking in bookings:
            response.append(
                f"• {booking.session_date.strftime('%d.%m.%Y %H:%M')}"
            )
        await message.answer("\n".join(response))
    else:
        await message.answer("😔 У вас нет активных записей")

# -------------------------
# Вспомогательные функции
# -------------------------

async def notify_booking_changes(booking_data: dict):
    """Уведомление об изменениях через вебхук"""
    async with get_async_db() as db:
        # Логика обработки изменений
        pass
