
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.database import get_db
from sqlalchemy import select
from api.db.models import Group, Date, GroupDateAssociation 



async def load_groups_and_dates(groups: dict, dates: dict, db: AsyncSession): 
    try:
        for date_text, date_data_value in dates.items():
            # Проверяем существует ли дата
            result = await db.scalars(
                select(Date).where(Date.data_value == date_data_value)
            )
            existing_date = result.first()
            
            if not existing_date:
                db_date = Date(date=date_text, data_value=date_data_value)
                db.add(db_date)

            # await db.refresh(db_date)
        
        
        # Затем создаем группы, а затем их связываем с датами 
        for group_number, group_data_value in groups.items():
            # Проверяем существует ли группа
            existing_group = await db.scalars(
                select(Group).where(Group.data_value == group_data_value)
            )
            if not existing_group.first():
                db_group = Group(group_number=group_number, data_value=group_data_value)
                db.add(db_group)

            # await db.refresh(db_group)
                
        await db.commit()
        
    except Exception as e: 
        await db.rollback() 
        print(str(e))
        raise
