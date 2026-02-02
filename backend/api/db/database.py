from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase
from ..logger import log
from ...core.config import settings

class Base(DeclarativeBase): ...


engine: AsyncEngine = create_async_engine(
    settings.db.url,
    future=settings.db.future,
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
log.info("Postgres engine initialized.")

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)



test_engine: AsyncEngine = create_async_engine(
    settings.db.test_url,
    future=settings.db.future,
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)

AsyncSessionLocalTest = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)

if settings.app.dev: 
    AsyncSessionLocal = AsyncSessionLocalTest


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session