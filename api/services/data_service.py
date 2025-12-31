from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.db.models import Group, Date

class DataService:
    @staticmethod
    async def get_all_groups(db: AsyncSession):
        result = await db.scalars(select(Group))
        result_all = result.all()

        # dumpdata = [gr.group_number for gr in result_all]
        # with open('templates/static/json/groups.json', 'w') as f:
        #     json.dump(dumpdata, f)
        
        return result_all
    
    @staticmethod
    async def get_all_dates(db: AsyncSession):
        result = await db.scalars(select(Date))
        return result

        

data_service = DataService() 
