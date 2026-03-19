from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api.db.models import Date, Group, Homework, User
from backend.api.logger import log


class TaskService:
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
