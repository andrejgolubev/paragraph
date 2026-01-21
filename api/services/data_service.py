from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.db.models import Group, Date

class DataService:
    @staticmethod
    async def get_all_groups(db: AsyncSession):
        result = await db.scalars(select(Group))
        if (result_all := result.all()): 
            return result_all
        return []
        
    
    @staticmethod
    async def get_all_dates(db: AsyncSession):
        result = await db.scalars(select(Date))
        if (result_all := result.all()): 
            return result_all
        return []

        

data_service = DataService() 
