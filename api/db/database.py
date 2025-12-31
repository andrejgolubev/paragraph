from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from api.settings import Settings

# DATABASE_URL = 'postgresql+asyncpg://postgres:root@127.0.0.1:5433/postgres'

engine = create_async_engine(Settings.db_url, future=True, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase): ...

# Dependency для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        
