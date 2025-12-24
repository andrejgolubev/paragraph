from fastapi import APIRouter, Depends, Request, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.db.database import get_db
from api.db.models import Group, Date, GroupDateAssociation
from typing import Optional
from datetime import datetime
from api.db.schemas import HomeworkRequest
    
homework_router = APIRouter(tags=["Homework"], prefix="/homework")
router = homework_router



@router.post("/save")
async def save_homework(
    request: Request,
    homework_request: HomeworkRequest = Body(),
    db: AsyncSession = Depends(get_db),
):
    group_data_value = homework_request.group_data_value
    date_data_value = homework_request.date_data_value
    lesson_index = homework_request.lesson_index
    homework = homework_request.homework
    try:
        # Находим группу
        group_result = await db.scalars(
            select(Group).where(Group.data_value == group_data_value)
        )
        group = group_result.first()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        # Находим дату
        date_result = await db.scalars(
            select(Date).where(Date.data_value == date_data_value)
        )
        date = date_result.first()

        if not date:
            raise HTTPException(status_code=404, detail="Date not found")

        # Находим или создаем связь
        association_result = await db.scalars(
            select(GroupDateAssociation).where(
                GroupDateAssociation.group_id == int(group.id),
                GroupDateAssociation.dates_id == date.id,
                GroupDateAssociation.lesson == lesson_index,
            )
        )
        association = association_result.first()

        if not association:
            association = GroupDateAssociation(
                group_id=group.id,
                dates_id=date.id,
                lesson=lesson_index,
                homework=homework,
                updated=datetime.now()
            )
            db.add(association)
        else:
            association.homework = homework or ""
            association.updated = datetime.now()

        await db.commit()

        return {"status": "success", "message": "Homework saved"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving homework: {str(e)}")


@router.get("/get")
async def get_homework(
    group_data_value: str,
    date_data_value: str,
    lesson_index: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    try:
        # Аналогичная логика поиска связи и возврата homework
        group_result = await db.scalars(
            select(Group).where(Group.data_value == group_data_value)
        )
        group = group_result.first()

        date_result = await db.scalars(
            select(Date).where(Date.data_value == date_data_value)
        )
        date = date_result.first()

        if not group or not date:
            return {"failure": "group or date not selected or not found"}

        association_result = await db.scalars(
            select(GroupDateAssociation).where(
                GroupDateAssociation.group_id == group.id,
                GroupDateAssociation.dates_id == date.id,
                GroupDateAssociation.lesson == lesson_index,
            )
        )
        association = association_result.first() 

        return {
            "homework": association.homework if association else "",
            "updated": association.updated if association.updated else "" #type:ignore
        }

    except Exception as e:
        return {"homework": "", "exception": e}
