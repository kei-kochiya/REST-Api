from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from database.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./proseka.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args = {"check_same_thread": False}
)

SessionLocal = async_sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine,
    class_ = AsyncSession
)

async def get_db():
    async with SessionLocal() as db:
        yield db