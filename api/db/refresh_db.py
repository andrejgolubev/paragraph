from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, delete, select
from api.db.models import Group, Date, GroupDateAssociation
from datetime import datetime

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



async def cleanup_dates_by_period(
    db: AsyncSession,
    start_date: str | None = None,  # формат: "dd.mm.yyyy" или "yyyy-mm-dd"
    end_date: str | None = None,    # формат: "dd.mm.yyyy" или "yyyy-mm-dd"
) -> dict:
    """
    очистка дат и связанных записей за указанный период.
     """
        
    if start_date and end_date:
        # по конкретному промежутку пытаемся понять формат даты
        try:
            # пытаемся распарсить как dd.mm.yyyy
            start_dt = datetime.strptime(start_date, "%d.%m.%Y")
            end_dt = datetime.strptime(end_date, "%d.%m.%Y")
            # преобразуем в оба формата для условий
            start_date_str = start_dt.strftime("%d.%m.%Y")
            start_value_str = start_dt.strftime("%Y-%m-%d")
            end_date_str = end_dt.strftime("%d.%m.%Y")
            end_value_str = end_dt.strftime("%Y-%m-%d")
            
            conditions = and_(
                Date.date >= start_date_str,
                Date.date <= end_date_str
            )
            
        except ValueError:
            # пытаемся распарсить как yyyy-mm-dd
            try:
                start_dt = datetime.strptime(start_date, "%Y-%m-%d")
                end_dt = datetime.strptime(end_date, "%Y-%m-%d")
                start_date_str = start_dt.strftime("%d.%m.%Y")
                start_value_str = start_dt.strftime("%Y-%m-%d")
                end_date_str = end_dt.strftime("%d.%m.%Y")
                end_value_str = end_dt.strftime("%Y-%m-%d")
                
                conditions = and_(
                    Date.data_value >= start_value_str,
                    Date.data_value <= end_value_str
                )
            except ValueError:
                return {"error": "Неверный формат даты. Используйте dd.mm.yyyy или yyyy-mm-dd"}
    else:
        return {"error": "Не указан период для очистки"}
    
    try:
        # находим ID дат для удаления
        date_ids_result = await db.execute(
            select(Date.id).where(conditions)
        )
        date_ids = [row[0] for row in date_ids_result.all()]
        
        if not date_ids:
            return {"message": "Нет дат для удаления в указанном периоде"}
        
        # удаляем связанные записи из GroupDateAssociation
        association_deleted = await db.execute(
            delete(GroupDateAssociation).where(
                GroupDateAssociation.dates_id.in_(date_ids)
            )
        )
        associations_count = association_deleted.rowcount # количество удаленных связей
        
        # удаляем сами даты
        await db.execute(
            delete(Date).where(Date.id.in_(date_ids))
        )
        
        await db.commit()
        
        return {
            "message": "Очистка выполнена успешно",
            "period": {
                "start_date": start_date,
                "end_date": end_date,
                "start_value_str": start_value_str,
                "end_value_str": end_value_str
            },
            "deleted": {
                "dates_count": len(date_ids),
                "associations_count": associations_count
            }
        }
        
    except Exception:
        await db.rollback()
        return {"error": "Ошибка при очистке."}