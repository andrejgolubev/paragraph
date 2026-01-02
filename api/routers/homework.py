from fastapi import APIRouter, Depends, Request, HTTPException, Body, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.auth.validation import get_current_active_auth_user
from api.db.database import get_db
from api.db.models import Group, Date, GroupDateAssociation
from datetime import datetime
from api.db.schemas import HomeworkRequest

router = homework_router = APIRouter(tags=["Homework"], prefix="/homework")


@router.post("/save")
async def save_homework(
    response: Response,
    user: dict = Depends(get_current_active_auth_user),
    homework_request: HomeworkRequest = Body(),
    db: AsyncSession = Depends(get_db),
):
    if not user:
        raise HTTPException(status_code=401, detail="пожалуйста, войдите в аккаунт")

    if "admin" not in (role := user["role"]):
        raise HTTPException(status_code=403, detail="недостаточно прав для управления этим д/з.")

    group_data_value = homework_request.group_data_value
    date_data_value = homework_request.date_data_value
    lesson_index = homework_request.lesson_index
    homework = homework_request.homework

    moderated_group_numbers = [gr for gr in role.split(".")[1:] if gr] # недоразумение 
    moderated_group_datavalues = [await get_group_datavalue(group_number, db=db) for group_number in moderated_group_numbers]

    
    if not any([group_dv for group_dv in moderated_group_datavalues if group_data_value == group_dv]): 
        raise HTTPException(status_code=403, detail="недостаточно прав для управления этим д/з.")
        

    try:
        group_result = await db.scalars(
            select(Group).where(Group.data_value == group_data_value)
        )

        if not (group := group_result.first()):
            raise HTTPException(status_code=404, detail="Group not found")

        date_result = await db.scalars(
            select(Date).where(Date.data_value == date_data_value)
        )

        if not (date := date_result.first()):
            raise HTTPException(status_code=404, detail="Date not found")

        # находим или создаем связь
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
                updated=datetime.now(),
            )
            db.add(association)
        else:
            association.homework = homework or ""
            association.updated = datetime.now()

        # public_cookies = {
        #     "group_data_value": group_data_value,
        #     "date_data_value": date_data_value,
        # }

        # for key, value in public_cookies.items():
        #     response.set_cookie(
        #         key=key,
        #         value=value,
        #         httponly=False,  # тк JS может читать эти куки чтоб в соответствии с выбранной группой и датой пользователем сразу отображалась нужная таблица
        #         secure=True,  # для htpps
        #         samesite="none",  
        #         max_age=60*60*24*14 # 14 days
        #     )

        await db.commit()

        return {"detail": "saved", "user": user}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"ошибка сохранения д/з: {e}")


async def get_group_datavalue(
    group_number: str,
    db: AsyncSession = Depends(get_db),
):
    print(f' ИЗ get_group_datavalue: {group_number = }')
    group_result = await db.scalars(
        select(Group).where(Group.group_number == group_number)
    )

    
    group_data_value = group_result.first().data_value
    print(f'{group_data_value = }')
    return group_data_value


@router.get("/convert")
async def convert_to_datavalue(
    group_number: str | None = None,
    date: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """ПЕРЕВОДИТ группы и даты в data_value-формат"""

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
    """ПЕРЕВОДИТ группы и даты из data_value-формата"""
    group_result = await db.scalars(
        select(Group).where(Group.data_value == group_data_value)
    )
    db_group = group_result.first()

    date_result = await db.scalars(select(Date).where(Date.data_value == date_data_value))

    db_date = date_result.first()

    if not db_group and not db_date:
        return {"failure": "group and date not selected or not found"}

    return {
        "date_data_value": db_date.date if db_date else "",
        "group_data_value": db_group.group_number if db_group else "",
    }


@router.get("/get")
async def get_homework(
    group_data_value: str,
    date_data_value: str,
    lesson_index: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
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
            "updated": (
                association.updated if association.updated else ""
            ),  # type:ignore
        }

    except Exception as e:
        return {"homework": "", "exception": e}
