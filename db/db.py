from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import settings

engine = create_async_engine(settings.REAL_DATABASE_URL, future=True, echo=True)

 # session fabric
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)



async def get_db():
    """Dependency for getting async session"""
    async with async_session() as session: 
        yield session
