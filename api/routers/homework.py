from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.db.database import get_db
from api.db.models import Group, Date, GroupDateAssociation
from typing import Optional



homework_router = APIRouter(tags=['Homework'], prefix='/homework')
router = homework_router 


@router.post("/save-homework")
async def save_homework(
    homework_data: dict,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        group_data_value = homework_data.get("group_data_value")
        date_data_value = homework_data.get("date_data_value")
        homework_text = homework_data.get("homework")
        
        # Находим группу
        group_result = await db.execute(
            select(Group).where(Group.data_value == group_data_value)
        )
        group = group_result.scalar_one_or_none()
        
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        
        # Находим дату
        date_result = await db.execute(
            select(Date).where(Date.data_value == date_data_value)
        )
        date = date_result.scalar_one_or_none()
        
        if not date:
            raise HTTPException(status_code=404, detail="Date not found")
        
        # Находим или создаем связь
        association_result = await db.execute(
            select(GroupDateAssociation).where(
                GroupDateAssociation.group_id == group.id,
                GroupDateAssociation.dates_id == date.id
            )
        )
        association = association_result.scalar_one_or_none()
        
        if not association:
            association = GroupDateAssociation(
                group_id=group.id,
                dates_id=date.id,
                # lesson_index еще тут
                homework=homework_text
            )
            db.add(association)
        else:
            association.homework = homework_text or ""
        
        await db.commit()
        
        return {"status": "success", "message": "Homework saved"}
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving homework: {str(e)}")


@router.get("/get-homework")
async def get_homework(
    group_data_value: str,
    date_data_value: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    try:
        # Аналогичная логика поиска связи и возврата homework
        group_result = await db.execute(
            select(Group).where(Group.data_value == group_data_value)
        )
        group = group_result.scalar_one_or_none()
        
        date_result = await db.execute(
            select(Date).where(Date.data_value == date_data_value)
        )
        date = date_result.scalar_one_or_none()
        
        if not group or not date:
            return {'failure': 'group or date not selected or not found'}
        
        association_result = await db.execute(
            select(GroupDateAssociation).where(
                GroupDateAssociation.group_id == group.id,
                GroupDateAssociation.dates_id == date.id
            )
        )
        association = association_result.scalar_one_or_none()
        
        return {"homework": association.homework if association else ""}
        
    except Exception as e:
        return {"homework": "", 'exception': e}