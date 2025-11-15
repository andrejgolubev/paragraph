from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.db.models import Group, Date

class DataService:
    @staticmethod
    async def get_all_groups(db: AsyncSession):
        result = await db.scalars(select(Group))
        return result.all()
    
    @staticmethod
    async def get_all_dates(db: AsyncSession):
        result = await db.scalars(select(Date))
        return result.all()

data_service = DataService()