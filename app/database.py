from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import Config

# Синхронная версия для миграций и административных задач
sync_engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False}
)

# Асинхронная версия для работы бота
async_engine = create_async_engine(
    Config.SQLALCHEMY_DATABASE_URI.replace("sqlite://", "sqlite+aiosqlite://"),
    echo=False,
    future=True
)

# Сессии
SyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

def init_db():
    """Инициализация таблиц в базе данных"""
    Base.metadata.create_all(bind=sync_engine)

async def get_async_db():
    """Асинхронный генератор сессий для бота"""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

def get_sync_db():
    """Синхронный генератор сессий для веб-интерфейса"""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()