from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api.db.models import Date, Group, Homework, User
from backend.api.logger import log
from backend.api.schemas.homework import HomeworkRequest
from ..utils.converters import latin_to_cyrillic, get_group_datavalue_by_group_number


class TaskService:
    async def save_task(
        self,
        db: AsyncSession,
        current_user: User,
        homework_request: HomeworkRequest,
        is_note: bool,
    ):
        """
        Сохраняет или обновляет задание для указанной группы/даты
        """

        if not current_user.name:
            raise HTTPException(status_code=401, detail="пожалуйста, войдите в аккаунт")

        group_data_value = homework_request.group_data_value
        date_data_value = homework_request.date_data_value
        lesson_index = homework_request.lesson_index
        homework_text = homework_request.homework_text

        if not is_note:
            if "admin" not in (role := current_user.role):
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
                detail=f"задание не может быть больше {max_homework_length} символов.",
            )

        if not homework_text:
            detail = (
                "заметка не может быть пустой"
                if is_note
                else "д/з не может быть пустым"
            )
            raise HTTPException(status_code=400, detail=detail)

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
                    Homework.user_id == current_user.id,
                    Homework.lesson_index == lesson_index,
                    Homework.is_note == is_note,
                )
            )
            homework = hmw_result.first()

            if not homework:
                homework = Homework(
                    group_id=group.id,
                    dates_id=date.id,
                    user_id=current_user.id,
                    lesson_index=lesson_index,
                    homework_text=homework_text,
                    updated=datetime.now(),
                    is_note=is_note,
                )
                db.add(homework)
            else:
                homework.homework_text = homework_text
                homework.user_id = current_user.id
                homework.updated = datetime.now()

            await db.commit()

            return {
                "status": "ok",
                "detail": "saved",
                "message": "Заметка добавлена" if is_note else "Домашнее задание сохранено" ,
                "username": current_user.name,
            }

        except Exception:
            await db.rollback()
            raise HTTPException(status_code=500, detail="Ошибка сохранения.")


    async def get_task(
        self,
        db: AsyncSession,
        group_data_value: str,
        date_data_value: str,
        lesson_index: int,
        is_note: bool,
        current_user: User | None = None,
    ):
        """
        Возвращает:
        - текст задания
        - время добавления
        - автора (если is_note=False)
        для конкретной группы, даты и урока.
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

            stmt = select(Homework).where(
                Homework.group_id == group.id,
                Homework.dates_id == date.id,
                Homework.lesson_index == lesson_index,
                Homework.is_note == is_note,
            )
            if not is_note:
                stmt = stmt.options(selectinload(Homework.user))
            elif current_user is not None:
                stmt = stmt.where(Homework.user_id == current_user.id)

            task = (await db.scalars(stmt)).first()

            task_response = {
                "homework_text": task.homework_text if task else "",
                "updated": task.updated if task else "",
            }
            if not is_note:
                task_response |= {"username": task.user.name}

            return task_response

        except Exception as e:
            log.error("Error getting task: %s ", e)
            return {"homework_text": ""}

    async def get_all_task_indexes(
        self,
        db: AsyncSession,
        group_data_value: str,
        date_data_value: str,
        is_note: bool,
        current_user: User | None = None,
    ) -> dict:
        """
        Возвращает словарь с индексами домашек и булевыми ключами,
        отвечающими за наличие/отсутствие задания
        """
        try:
            group = (
                await db.scalars(
                    select(Group).where(Group.data_value == group_data_value)
                )
            ).first()

            date = (
                await db.scalars(select(Date).where(Date.data_value == date_data_value))
            ).first()

            if not group or not date:
                return {"detail": "Группа или дата не выбраны или не найдены"}

            stmt = select(Homework).where(
                Homework.group_id == group.id,
                Homework.dates_id == date.id,
                Homework.is_note == is_note,
            )
            if is_note:
                stmt = stmt.where(Homework.user_id == current_user.id)

            task_result = (await db.scalars(stmt)).all()

            return {task.lesson_index: bool(task.homework_text) for task in task_result}

        except Exception as e:
            log.error("Error saving task: %s ", e)
            return {}
