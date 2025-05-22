from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from config import DATA_DIR

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    full_name = Column(String)
    username = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.telegram_id'))
    session_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

class Database:
    def __init__(self):
        self.engine = create_engine(f"sqlite:///{DATA_DIR}/bookings.db")
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def get_user(self, telegram_id: int):
        with self.Session() as session:
            return session.query(User).filter_by(telegram_id=telegram_id).first()

    def add_user(self, telegram_id: int, full_name: str, username: str = None):
        with self.Session() as session:
            session.add(User(
                telegram_id=telegram_id,
                full_name=full_name,
                username=username
            ))
            session.commit()

    def get_upcoming_sessions(self, user_id: int = None):
        from datetime import datetime, timedelta
        with self.Session() as session:
            query = session.query(Booking).filter(
                Booking.session_date > datetime.now()
            )
            if user_id:
                query = query.filter_by(user_id=user_id)
            return query.all()
