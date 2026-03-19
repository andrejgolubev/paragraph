from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.api.db.models import Homework, Group, Date, User
from backend.api.auth.validation import get_current_auth_user
from backend.api.db.database import get_db


async def get_note_if_owner(
    group_data_value: str,
    date_data_value: str,
    lesson_index: int,
    current_user: User = Depends(get_current_auth_user),
    db: AsyncSession = Depends(get_db),
) -> Homework:
    """
    Возвращает заметку только если она принадлежит текущему пользователю
    """
    # Находим группу и дату
    group = (await db.scalars(
        select(Group).where(Group.data_value == group_data_value)
    )).first()
    
    date = (await db.scalars(
        select(Date).where(Date.data_value == date_data_value)
    )).first()
    
    if not group or not date:
        raise HTTPException(status_code=404, detail="Группа или дата не найдены")
    
    # Ищем заметку
    note = (await db.scalars(
        select(Homework).where(
            Homework.group_id == group.id,
            Homework.dates_id == date.id,
            Homework.lesson_index == lesson_index,
            Homework.is_note == True,
            Homework.user_id == current_user.id  # сразу фильтруем по пользователю
        )
    )).first()
    
    return note