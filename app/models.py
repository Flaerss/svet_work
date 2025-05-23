from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class Client(Base):
    """Клиенты фотостудии"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    yclients_id = Column(Integer, unique=True, comment="ID из YClients")
    telegram_id = Column(Integer, unique=True, index=True)
    phone = Column(String(20), comment="Формат: +79991234567")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Client {self.phone}>"

class Booking(Base):
    """Записи на фотосессии"""
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), index=True)
    session_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='active')  # active/canceled/changed

    def __repr__(self):
        return f"<Booking {self.session_date}>"from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class Client(Base):
    """Клиенты фотостудии"""
    __tablename__ = 'clients'
    
    id = Column(Integer, primary_key=True)
    yclients_id = Column(Integer, unique=True, comment="ID из YClients")
    telegram_id = Column(Integer, unique=True, index=True)
    phone = Column(String(20), comment="Формат: +79991234567")
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Client {self.phone}>"

class Booking(Base):
    """Записи на фотосессии"""
    __tablename__ = 'bookings'
    
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey('clients.id'), index=True)
    session_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default='active')  # active/canceled/changed

    def __repr__(self):
        return f"<Booking {self.session_date}>"