from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.api.tasks.tasks import TaskService
from backend.api.logger import log
from ..auth.validation import get_current_auth_user
from ..db.database import get_db
from ..db.models import Group, Date, Homework, User
from datetime import datetime
from ..schemas.homework import HomeworkRequest
from ..utils.converters import latin_to_cyrillic, get_group_datavalue_by_group_number


router = APIRouter(tags=["Notes"], prefix="/notes")


@router.post("/save")
async def save_note(
    user: User = Depends(get_current_auth_user),
    homework_request: HomeworkRequest = Body(),
    db: AsyncSession = Depends(get_db),
):
    """
    Сохраняет или обновляет заметку (индивидуальное д/з) пользователя
    для указанной группы/даты.
    """

    if not user.name:
        raise HTTPException(status_code=401, detail="пожалуйста, войдите в аккаунт")

    group_data_value = homework_request.group_data_value
    date_data_value = homework_request.date_data_value
    lesson_index = homework_request.lesson_index
    homework_text = homework_request.homework_text

    # валидация д/з
    if len(homework_text) > (max_homework_length := 750):
        raise HTTPException(
            status_code=400,
            detail=f"д/з не может быть больше {max_homework_length} символов",
        )

    if not homework_text:
        raise HTTPException(status_code=400, detail="д/з не может быть пустым")

    try:
        group_result = await db.scalars(
            select(Group).where(Group.data_value == group_data_value)
        )

        if not (group := group_result.first()):
            raise HTTPException(status_code=404, detail="Группа не найдена")

        date_result = await db.scalars(
            select(Date).where(Date.data_value == date_data_value)
        )

        if not (date := date_result.first()):
            raise HTTPException(
                status_code=404, detail="Дата не выбрана или не найдена"
            )

        # находим или создаем связь
        hmw_result = await db.scalars(
            select(Homework).where(
                Homework.group_id == group.id,
                Homework.dates_id == date.id,
                Homework.lesson_index == lesson_index,
                Homework.user_id == user.id,
                Homework.is_note == True,
            )
        )
        homework = hmw_result.first()

        if not homework:
            homework = Homework(
                group_id=group.id,
                dates_id=date.id,
                user_id=user.id,
                lesson_index=lesson_index,
                homework_text=homework_text,
                updated=datetime.now(),
                is_note=True,
            )
            db.add(homework)
        else:
            homework.homework_text = homework_text
            homework.user_id = user.id
            homework.updated = datetime.now()

        await db.commit()

        return {
            "status": "ok",
            "detail": "saved",
            "message": "Заметка добавлена",
            "username": user.name,
        }

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="ошибка сохранения заметки.")


@router.get("/get")
async def get_note(
    request: Request,
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
