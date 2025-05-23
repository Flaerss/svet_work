import os
from pathlib import Path

class Config:
    # Пути
    BASE_DIR = Path(__file__).parent.parent  # Корень проекта
    DATA_DIR = BASE_DIR / "data"            # Папка для данных (база, логи)
    LOGS_DIR = BASE_DIR / "logs"            # Логи приложения
    
    # Бот
    BOT_TOKEN = os.getenv("BOT_TOKEN")      # Токен Telegram-бота
    ADMIN_ID = int(os.getenv("ADMIN_ID"))   # ID администратора
    
    # YClients
    YCLIENTS_TOKEN = os.getenv("YCLIENTS_TOKEN")  # API-токен YClients
    COMPANY_ID = os.getenv("COMPANY_ID")          # ID компании в YClients
    
    # Веб-интерфейс
    WEB_SECRET_KEY = os.getenv("WEB_SECRET_KEY", "default-secret-key")  # Ключ для Flask
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATA_DIR}/bookings.db"      # Путь к БД

    # Twilio (WhatsApp)
    TWILIO_SID = os.getenv("TWILIO_SID")
    TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
    WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE")

    @classmethod
    def create_dirs(cls):
        """Создает необходимые директории."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)