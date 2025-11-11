from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DATABASE_URL = 'postgresql+asyncpg://pg:root@127.0.0.1:5433/pg'

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase): ...

# Dependency для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        
