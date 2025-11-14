from fastapi import FastAPI, Depends, Request, APIRouter
from api.routers.users import user_router
from api.routers.auth import oauth2_scheme
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.database import get_db
from sqlalchemy import select
from api.db.models import Group, Date, GroupDateAssociation 
from api.db.schemes import GroupCreate, GroupResponse

schedule_router = APIRouter(tags=['schedule'], prefix='/schedule')



@schedule_router.post('/')
async def load_groups_and_dates(groups: dict, dates: dict, db: AsyncSession = Depends(get_db)): 
    dates_map = {} # data_value: date объект 

    for date_text, date_data_value in dates.items():
        # Проверяем существует ли дата
        result = await db.scalars(
            select(Date).where(Date.data_value == date_data_value)
        )
        existing_date = result.first()
        
        if not existing_date:
            db_date: Date = Date(date=date_text, data_value=date_data_value)
            db.add(db_date)
            dates_map[date_data_value] = db_date
        else:
            dates_map[date_data_value] = existing_date
    
    await db.commit()
    
    # Затем создаем группы и связи
    for group_number, group_data_value in groups.items():
        # Проверяем существует ли группа
        existing_group = await db.scalars(
            select(Group).where(Group.data_value == group_data_value)
        )
        if not existing_group.first():
            db_group = Group(group_number=group_number, data_value=group_data_value)
            db.add(db_group)
            
            # Создаем связи со всеми датами
            for date_data_value, db_date in dates_map.items():
                association = GroupDateAssociation(
                    group_id=db_group.id,
                    dates_id=db_date.id
                )
                db.add(association)
    
    await db.commit()





@schedule_router.post('/')
async def leave_homework(text, group_number: int, date: str, db = Depends(get_db)): ...