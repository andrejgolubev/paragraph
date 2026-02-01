import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import Date, Group
from backend.api.db.refresh_db import load_groups_and_dates

from backend.tests.conftest import groups_initial


dates_initial = {
    "26.01.2026": "2026-01-26", 
    "02.02.2026": "2026-02-02",
    "09.02.2026": "2026-02-09",
}

groups_additional = {
    "5100": "3432",
    "5110": "3431",
    "5120": "3430",
}
dates_additional = {
    "16.02.2027": "2027-02-16",
    "23.02.2027": "2027-02-23",
    "02.03.2027": "2027-03-02",
}


@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_replaces_existing_records(
    db: AsyncSession, 
):
    """
    Проверяет то, что старые записи в БД будут перезаписываются новыми при
    использовании флага refresh=True (т.е. при выполнении команды make refresh-db). 

    Внимание: Если тестовая БД была заполнена реальными данными, то они будут удалены
    и заменены на тестовые! 
    Используйте ./backend/Makefile для конфигурации групп и дат в тестовой БД
    """

    await db.execute(delete(Group))
    await db.execute(delete(Date))
    await db.commit()

    await load_groups_and_dates(groups_initial, dates_initial, db, refresh=True)

    stored_groups = await db.scalars(select(Group.group_number))
    stored_dates = await db.scalars(select(Date.data_value))

    assert set(stored_groups.all()) == set(groups_initial)
    assert set(stored_dates.all()) == set(dates_initial.values())

    await load_groups_and_dates(groups_additional, dates_additional, db, refresh=True)

    stored_groups = await db.scalars(select(Group.group_number))
    stored_dates = await db.scalars(select(Date.data_value))

    assert set(stored_groups.all()) == set(groups_additional)
    assert set(stored_dates.all()) == set(dates_additional.values())

    await db.rollback()



@pytest.mark.asyncio(loop_scope="session")
async def test_load_without_refresh_appends_missing_records(
    db: AsyncSession,
):
    """
    Проверяет, что новые данные заполняют недостающие записи в уже когда-то наполненной
    данными БД. Фактически проверяет работу флага refresh=True на непустой БД.

    Внимание: Если тестовая БД была заполнена реальными данными, то они будут удалены
    и заменены на тестовые! 
    Используйте ./backend/Makefile для конфигурации групп и дат в тестовой БД
    """

    await db.execute(delete(Group))
    await db.execute(delete(Date))
    await db.commit()

    await load_groups_and_dates(groups_initial, dates_initial, db, refresh=True)
    await load_groups_and_dates(groups_additional, dates_additional, db, refresh=False)

    stored_groups = await db.scalars(select(Group.group_number))
    stored_dates = await db.scalars(select(Date.data_value))

    expected_groups = set(groups_initial) | set(groups_additional)
    expected_dates = set(dates_initial.values()) | set(dates_additional.values())

    assert set(stored_groups.all()) == expected_groups
    assert set(stored_dates.all()) == expected_dates

    await db.rollback()