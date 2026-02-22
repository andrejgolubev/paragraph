from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from ..auth.validation import get_current_active_auth_user_data
from ..db.database import get_db
from ..db.models import Group, Date, Homework
from datetime import datetime
from ..db.schemas import HomeworkRequest
from ..utils.converters import latin_to_cyrillic, get_group_datavalue_by_group_number


router = homework_router = APIRouter(tags=["Homework"], prefix="/homework")


@router.post("/save")
async def save_homework(
    user_data: dict = Depends(get_current_active_auth_user_data),
    homework_request: HomeworkRequest = Body(),
    db: AsyncSession = Depends(get_db),
):
    """
    Сохраняет или обновляет домашнее задание для указанной группы/даты 
    в пределах прав администратора.
    """
    if not user_data:
        raise HTTPException(status_code=401, detail="пожалуйста, войдите в аккаунт")

    if "admin" not in (role := user_data["role"]):
        raise HTTPException(
            status_code=403, 
            detail="недостаточно прав для управления этим д/з."
        )

    group_data_value = homework_request.group_data_value
    date_data_value = homework_request.date_data_value
    lesson_index = homework_request.lesson_index
    homework_text = homework_request.homework

    if len(homework_text) > (max_homework_length := 750):
        raise HTTPException(status_code=400, detail=f"д/з не может быть больше {max_homework_length} символов")

    if not homework_text:
        raise HTTPException(status_code=400, detail="д/з не может быть пустым")

    moderated_group_numbers = [
        latin_to_cyrillic(gr) for gr in role.split(".")[1:] if gr
    ] 
    moderated_group_datavalues = [
        await get_group_datavalue_by_group_number(group_number, db=db) 
        for group_number in moderated_group_numbers
    ]


    if not any(
        [group_dv for group_dv in moderated_group_datavalues 
        if group_data_value == group_dv]
    ): 
        raise HTTPException(
            status_code=403, 
            detail="недостаточно прав для управления этим д/з."
        )
        

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
                status_code=404, 
                detail="Дата не выбрана или не найдена"
            )

        # находим или создаем связь
        hmw_result = await db.scalars(
            select(Homework).where(
                Homework.group_id == group.id,
                Homework.dates_id == date.id,
                Homework.lesson == lesson_index,
            )
        )
        homework = hmw_result.first()

        if not homework:
            homework = Homework(
                group_id=group.id,
                dates_id=date.id,
                user_id=user_data.get('id'),
                lesson=lesson_index,
                homework=homework_text,
                updated=datetime.now(),
            )
            db.add(homework)
        else:
            homework.homework = homework_text or ""
            homework.updated = datetime.now()


        await db.commit()

        return {
            "status": 'ok', 
            "detail": "saved", 
            "message": 'Домашнее задание сохранено',
            "username": user_data.get('username')
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
    try:
        # аналогичная логика поиска связи и возврата homework
        group_result = await db.scalars(
            select(Group).where(Group.data_value == group_data_value)
        )
        group = group_result.first()

        date_result = await db.scalars(
            select(Date).where(Date.data_value == date_data_value)
        )
        date = date_result.first()

        if not group or not date:
            return {"detail": "Группа или дата не выбраны или не найдены"}

        hmw_result = await db.scalars(
            select(Homework).where(
                Homework.group_id == group.id,
                Homework.dates_id == date.id,
                Homework.lesson == lesson_index,
            ).options(selectinload(Homework.user))
        )
        homework = hmw_result.first()

        return {
            "homework": homework.homework if homework else "",
            "updated": (
                homework.updated if homework else ""
            ),  
            'username': homework.user.name
        }

    except Exception:
        return {"homework": ""}


@router.get("/get-all")
async def get_all_homeworks_for_schedule(
    group_data_value: str,
    date_data_value: str,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Возвращает словарь с индексами домашек и булевыми ключами, 
    отвечающими за наличие/отсутствие домашки 
    """
    try:
        group_result = await db.scalars(
            select(Group).where(Group.data_value == group_data_value)
        )
        group = group_result.first()

        date_result = await db.scalars(
            select(Date).where(Date.data_value == date_data_value)
        )
        date = date_result.first()

        if not group or not date:
            return {"detail": "Группа или дата не выбраны или не найдены"}


        hmw_result = (await db.scalars(
            select(Homework).where(
                Homework.group_id == group.id,
                Homework.dates_id == date.id,
            )
        )).all()


        return {
            hmw.lesson: bool(hmw.homework) # lesson = lesson_id
            for hmw in hmw_result
        }
        

    except Exception:
        return {}




@router.get("/convert")
async def convert_to_datavalue(
    group_number: str | None = None,
    date: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    По заданному номеру группы и дате возвращает соответствующие значения data_value.
    """

    group_result = await db.scalars(
        select(Group).where(Group.group_number == group_number)
    )
    db_group = group_result.first()

    date_result = await db.scalars(select(Date).where(Date.date == date))

    db_date = date_result.first()

    if not db_group and not db_date:
        raise HTTPException(
            status_code=404,
            detail="at least group or date has to be selected (or they were just not found)",
        )

    return {
        "date_data_value": db_date.data_value if db_date else "",
        "group_data_value": db_group.data_value if db_group else "",
    }


@router.get("/convert-back")
async def convert_from_datavalue(
    group_data_value: str | None = None,
    date_data_value: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """По значениям data_value находит читаемые номер группы и дату."""
    group_result = await db.scalars(
        select(Group).where(Group.data_value == group_data_value)
    )
    db_group = group_result.first()

    date_result = await db.scalars(
        select(Date).where(Date.data_value == date_data_value)
    )

    db_date = date_result.first()

    if not db_group and not db_date:
        return {"failure": "group and date not selected or not found"}

    return {
        "date": db_date.date if db_date else "",
        "group_number": db_group.group_number if db_group else "",
    }