from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
import logging
from database import Database

logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    async def start(self, bot: Bot):
        self.scheduler.add_job(
            self._send_reminders, 
            'interval', 
            minutes=30, 
            args=[bot]
        )
        self.scheduler.start()
        logger.info("Планировщик запущен")

    async def _send_reminders(self, bot: Bot):
        """Отправка напоминаний"""
        try:
            db = Database()
            bookings = db.get_upcoming_sessions(hours=1)
            for booking in bookings:
                await bot.send_message(
                    chat_id=booking.user_id,
                    text=f"⏰ Через час ваша фотосессия!"
                )
        except Exception as e:
            logger.error(f"Ошибка: {e}")

scheduler = Scheduler()
