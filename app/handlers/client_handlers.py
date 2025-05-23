from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("📸 Добро пожаловать в фотостудию SVET!\n\nДоступные команды:\n/booking - Записаться\n/my_bookings - Мои записи")

@router.message(Command("booking"))
async def booking_handler(message: types.Message):
    await message.answer("📅 Введите дату в формате ДД.ММ.ГГГГ ЧЧ:ММ")
