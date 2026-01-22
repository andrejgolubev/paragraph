from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from ...api.logger import log
from backend.core.config import settings

class Base(DeclarativeBase): ...


DB_URL = (
    f"{settings.db.scheme}://{settings.db.user}:{settings.db.password}"
    f"@{settings.db.host}:{settings.db.port}/{settings.db.name}"
)


engine: AsyncEngine = create_async_engine(
    DB_URL,
    future=settings.db.future,
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
log.info("Postgres engine initialized.")

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
