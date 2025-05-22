from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
import logging
import os

logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
    
    async def start(self, bot: Bot):
        self.scheduler.add_job(
            self._keep_alive, 
            'interval', 
            minutes=10, 
            args=[bot]
        )
        self.scheduler.start()
        logger.info("Планировщик запущен")
    
    async def shutdown(self):
        self.scheduler.shutdown()
        logger.info("Планировщик остановлен")
    
    async def _keep_alive(self, bot: Bot):
        logger.info("Поддержание активности...")

scheduler = Scheduler()
