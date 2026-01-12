from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete, select
from api.db.models import Group, Date, GroupDateAssociation
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession


async def load_groups_and_dates(groups: dict, dates: dict, db: AsyncSession, refresh: bool = False): 
    try:
        if refresh:
            await db.execute(delete(Date))
            await db.execute(delete(Group))
            await db.commit()
        for date_text, date_data_value in dates.items():
            # проверяем существует ли дата
            result = await db.scalars(
                select(Date).where(Date.data_value == date_data_value)
            )
            existing_date = result.first()
            db_date = Date(date=date_text, data_value=date_data_value)
            if refresh or not existing_date:
                db.add(db_date)
        
        # создаем группы, а затем их связываем с датами 
        for group_number, group_data_value in groups.items():
            # проверяем существует ли группа
            result = await db.scalars(
                select(Group).where(Group.data_value == group_data_value)
            )
            existing_group = result.first()
            db_group = Group(group_number=group_number, data_value=group_data_value)
            if refresh or not existing_group: 
                db.add(db_group)
            

        await db.commit()
        
    except Exception: 
        await db.rollback() 
        raise



async def clean_up_date(date_input: str, db: AsyncSession):
    try: 
        result = await db.scalars(
            select(Date).where(Date.data_value == date_input)
        )
        existing_date = result.first()
        if existing_date:
            await db.execute(delete(GroupDateAssociation).where(GroupDateAssociation.dates_id == existing_date.id))
            await db.execute(delete(Date).where(Date.id == existing_date.id))
            await db.commit()
            return {"message": "Очистка выполнена успешно"}
        else:
            return {"message": "Дата не найдена"}
    except Exception:
        await db.rollback()
        raise


async def clean_up_dates(dates_amount: int, db: AsyncSession):
    try:
        dates_result = await db.scalars(
            select(Date).order_by(Date.id).limit(dates_amount)
        )
        dates = dates_result.all()
        for date in dates:
            await db.execute(delete(GroupDateAssociation).where(GroupDateAssociation.dates_id == date.id))
            await db.execute(delete(Date).where(Date.id == date.id))

        await db.commit()
        return {"message": "Очистка выполнена успешно"}
    except Exception:
        await db.rollback()
        raise