from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from datetime import datetime, timedelta
from api.db.models import Group, Date, GroupDateAssociation 

async def cleanup_old_associations(db: AsyncSession, days_old: int = 30):
    """
    Удаляет только устаревшие связи из ассоциативной таблицы,
    НЕ трогая сами группы и даты
    """
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    result = await db.execute(
        delete(GroupDateAssociation).where(
            GroupDateAssociation.created_at < cutoff_date
        )
    )
    
    await db.commit()
    
    deleted_count = result.rowcount
    print(f"Удалено {deleted_count} комбинаций группа-дата из ассоциативной таблицы.")
    return deleted_count