from database import Database  # Добавьте импорт

class Scheduler:
    async def _send_reminders(self, bot: Bot):
        """Отправка напоминаний о бронированиях"""
        try:
            db = Database()
            upcoming = db.get_upcoming_sessions(hours=1)  # Сеансы в ближайший час
            for booking in upcoming:
                user = db.get_user(booking.user_id)
                await bot.send_message(
                    chat_id=user.telegram_id,
                    text=f"⏰ Через час ваша фотосессия в {booking.session_date.strftime('%H:%M')}"
                )
        except Exception as e:
            logger.error(f"Ошибка отправки напоминаний: {e}")

    async def start(self, bot: Bot):
        self.scheduler.add_job(
            self._send_reminders, 
            'interval', 
            minutes=30, 
            args=[bot]
        )
        self.scheduler.start()
