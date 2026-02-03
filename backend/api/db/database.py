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


def _make_engine(db_url): 
    return create_async_engine(
        db_url,
        future=settings.db.future,
        echo=settings.db.echo,
        pool_size=settings.db.pool_size,
        max_overflow=settings.db.max_overflow,
    )


engine: AsyncEngine = _make_engine(settings.db.url)
log.info("Postgres engine initialized.")

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


test_engine: AsyncEngine = _make_engine(settings.db.test_url)
log.info("Postgres TEST engine initialized.")

AsyncSessionLocalTest = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)



async def get_db():
    async with AsyncSessionLocal() as session:
        yield session