from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..auth.validation import get_current_auth_user
from ..db.database import get_db
from ..db.models import Group, Date, Homework, User
from datetime import datetime
from ..schemas.homework import HomeworkRequest
from ..utils.converters import latin_to_cyrillic, get_group_datavalue_by_group_number
from .helpers import DvConverter
from .tasks import TaskService

router = APIRouter(tags=["Homework"], prefix="/homework")


@router.post("/save")
async def save_homework(
    user: User = Depends(get_current_auth_user),
    homework_request: HomeworkRequest = Body(),
    db: AsyncSession = Depends(get_db),
):
    """
    Сохраняет или обновляет домашнее задание для указанной группы/даты
    в пределах прав администратора.
    """
    if not user.name:
        raise HTTPException(status_code=401, detail="пожалуйста, войдите в аккаунт")

    group_data_value = homework_request.group_data_value
    date_data_value = homework_request.date_data_value
    lesson_index = homework_request.lesson_index
    homework_text = homework_request.homework_text


    if "admin" not in (role := user.role):
        raise HTTPException(
            status_code=403, detail="недостаточно прав для управления этим д/з."
        )

    # проверка прав на редактирование
    moderated_group_numbers = [
        latin_to_cyrillic(gr) for gr in role.split(".")[1:] if gr
    ]
    moderated_group_datavalues = [
        await get_group_datavalue_by_group_number(group_number, db=db)
        for group_number in moderated_group_numbers
    ]

    if not any(
        [
            group_dv
            for group_dv in moderated_group_datavalues
            if group_data_value == group_dv
        ]
    ):
        raise HTTPException(
            status_code=403, detail="недостаточно прав для управления этим д/з."
        )

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
                Homework.is_note == False,
                
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
                is_note=False,
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
            "message": "Домашнее задание сохранено",
            "username": user.name
        }

    except Exception:
        await db.rollback()
        raise HTTPException(status_code=500, detail="ошибка сохранения д/з.")


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
