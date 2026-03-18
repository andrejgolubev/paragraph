from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import Date, Group

class DvConverter: 
    async def convert_to_datavalue(
        db: AsyncSession,
        group_number: str | None = None,
        date: str | None = None,
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


    async def convert_from_datavalue(
        db: AsyncSession,
        group_data_value: str | None = None,
        date_data_value: str | None = None,
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