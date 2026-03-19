from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..auth.validation import get_current_auth_user
from ..db.database import get_db
from ..db.models import User
from ..schemas.homework import HomeworkRequest
from ..utils.converters import latin_to_cyrillic, get_group_datavalue_by_group_number
from .helpers import DvConverter
from .service import TaskService

router = APIRouter(tags=["Homework"], prefix="/homework")


@router.post("/save")
async def save_homework(
    current_user: User = Depends(get_current_auth_user),
    homework_request: HomeworkRequest = Body(),
    db: AsyncSession = Depends(get_db),
):
    """
    Сохраняет или обновляет домашнее задание для указанной группы/даты
    в пределах прав администратора.
    """
    return await TaskService().save_task(
        db, 
        current_user, 
        homework_request, 
        is_note=False,
    )


@router.get("/get")
async def get_homework(
    group_data_value: str,
    date_data_value: str,
    lesson_index: int,
    db: AsyncSession = Depends(get_db),
):
    """
    Возвращает текст домашнего задания, время и автора для конкретной группы,
    даты и урока.
    """
    return await TaskService().get_task(
        db, 
        group_data_value,
        date_data_value,
        lesson_index,
        is_note=False
    )


@router.get("/presence")
async def get_all_homework_indexes(
    group_data_value: str,
    date_data_value: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Возвращает словарь с индексами домашек и булевыми ключами,
    отвечающими за наличие/отсутствие домашки
    """
    return await TaskService().get_all_task_indexes(
        db, 
        group_data_value, 
        date_data_value, 
        is_note=False
    )


@router.get("/convert")
async def convert_to_datavalue(
    group_number: str | None = None,
    date: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    По заданному номеру группы и дате возвращает соответствующие значения data_value.
    """
    return await DvConverter().convert_to_datavalue(
        db,
        group_number,
        date,
    )
    


@router.get("/convert-back")
async def convert_from_datavalue(
    group_data_value: str | None = None,
    date_data_value: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """По значениям data_value находит читаемые номер группы и дату."""
    return await DvConverter().convert_from_datavalue(
        db,
        group_data_value,
        date_data_value,
    )
