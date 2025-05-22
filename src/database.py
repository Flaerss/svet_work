import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from config import DATA_DIR

# Создаем базовый класс для моделей
Base = declarative_base()

class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    full_name = Column(String(255))
    username = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Booking(Base):
    """Модель бронирования"""
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'), nullable=False)
    session_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Database:
    """Класс для работы с базой данных"""
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{DATA_DIR}/bookings.db')
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        """Создает таблицы в базе данных"""
        Base.metadata.create_all(self.engine)

    def get_user(self, telegram_id: int):
        """Получает пользователя по Telegram ID"""
        with self.Session() as session:
            return session.query(User).filter_by(telegram_id=telegram_id).first()

    def add_user(self, telegram_id: int, full_name: str, username: str = None):
        """Добавляет нового пользователя"""
        with self.Session() as session:
            user = User(
                telegram_id=telegram_id,
                full_name=full_name,
                username=username
            )
            session.add(user)
            session.commit()

    def add_booking(self, user_id: int, session_date: str):
        """Добавляет новое бронирование"""
        with self.Session() as session:
            booking = Booking(
                user_id=user_id,
                session_date=session_date
            )
            session.add(booking)
            session.commit()

    def get_upcoming_sessions(self, hours: int = 24):
        """Получает предстоящие сеансы"""
        from datetime import datetime, timedelta
        now = datetime.now()
        future = now + timedelta(hours=hours)
        
        with self.Session() as session:
            return session.query(Booking).filter(
                Booking.session_date.between(now, future)
            ).all()
