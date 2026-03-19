from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.tasks.service import TaskService
from ..auth.validation import get_current_auth_user
from ..db.database import get_db
from ..db.models import User
from ..schemas.homework import HomeworkRequest


router = APIRouter(tags=["Notes"], prefix="/notes")


@router.post("/save")
async def save_note(
    current_user: User = Depends(get_current_auth_user),
    homework_request: HomeworkRequest = Body(),
    db: AsyncSession = Depends(get_db),
):
    """
    Сохраняет или обновляет заметку (индивидуальное д/з) пользователя
    для указанной группы/даты.
    """

    return await TaskService().save_task(
        db, 
        current_user, 
        homework_request, 
        is_note=True,
    )


@router.get("/get")
async def get_note(
    group_data_value: str,
    date_data_value: str,
    lesson_index: int,
    current_user: User = Depends(get_current_auth_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Возвращает текст заметки и время добавления для конкретной 
    группы, даты и урока.
    """
    return await TaskService().get_task(
        db, 
        group_data_value,
        date_data_value,
        lesson_index,
        is_note=True,
        current_user=current_user,
    )


@router.get("/presence")
async def get_all_notes_indexes(
    group_data_value: str,
    date_data_value: str,
    current_user: User = Depends(get_current_auth_user),
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
        is_note=True,
        current_user=current_user
    )
