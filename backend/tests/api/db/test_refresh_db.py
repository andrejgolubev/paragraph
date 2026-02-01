import pytest
from contextlib import nullcontext as does_not_raise

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.db.models import Date, Group
from backend.api.db.refresh_db import (
    load_groups_and_dates,
    clean_up_date,
    clean_up_dates,
)

from backend.tests.conftest import GROUPS_INITIAL


"""
Внимание: Если тестовая БД была заполнена реальными данными, то они будут удалены
и заменены на тестовые! 
Используйте ./backend/Makefile для конфигурации групп и дат в тестовой БД
"""

DATES_INITIAL = {
    "26.01.2026": "2026-01-26", 
    "02.02.2026": "2026-02-02",
    "09.02.2026": "2026-02-09",
}

GROUPS_ADDITIONAL = {
    "5100": "3432",
    "5110": "3431",
    "5120": "3430",
}
DATES_ADDITIONAL = {
    "16.02.2027": "2027-02-16",
    "23.02.2027": "2027-02-23",
    "02.03.2027": "2027-03-02",
}


CLEANUP_DATES_PAYLOAD = [
    ("05.04.2027", "2027-04-05"),
    ("12.04.2027", "2027-04-12"),
    ("19.04.2027", "2027-04-19"),
]


async def _seed_dates_for_cleanup(db: AsyncSession) -> list[str]:
    """Добавляет в БД даты для тестирования и возвращает список этих дат"""
    await db.execute(delete(Date))
    await db.commit()
    inserted_values: list[str] = []
    for date_text, data_value in CLEANUP_DATES_PAYLOAD:
        db.add(Date(date=date_text, data_value=data_value))
        inserted_values.append(data_value)
    await db.commit()
    return inserted_values


@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_replaces_existing_records(
    db: AsyncSession, 
):
    """
    Проверяет то, что старые записи в БД будут перезаписываются новыми при
    использовании флага refresh=True (т.е. при выполнении команды make refresh-db). 
    
    """

    await db.execute(delete(Group))
    await db.execute(delete(Date))
    await db.commit()

    await load_groups_and_dates(GROUPS_INITIAL, DATES_INITIAL, db, refresh=True)

    stored_groups = await db.scalars(select(Group.group_number))
    stored_dates = await db.scalars(select(Date.data_value))

    assert set(stored_groups.all()) == set(GROUPS_INITIAL)
    assert set(stored_dates.all()) == set(DATES_INITIAL.values())

    await load_groups_and_dates(GROUPS_ADDITIONAL, DATES_ADDITIONAL, db, refresh=True)

    stored_groups = await db.scalars(select(Group.group_number))
    stored_dates = await db.scalars(select(Date.data_value))

    assert set(stored_groups.all()) == set(GROUPS_ADDITIONAL)
    assert set(stored_dates.all()) == set(DATES_ADDITIONAL.values())

    await db.rollback()



@pytest.mark.asyncio(loop_scope="session")
async def test_load_without_refresh_appends_missing_records(
    db: AsyncSession,
):
    """
    Проверяет, что новые данные заполняют недостающие записи в уже когда-то наполненной
    данными БД. Фактически проверяет работу флага refresh=True на непустой БД.

    """

    await db.execute(delete(Group))
    await db.execute(delete(Date))
    await db.commit()

    await load_groups_and_dates(GROUPS_INITIAL, DATES_INITIAL, db, refresh=True)
    await load_groups_and_dates(GROUPS_ADDITIONAL, DATES_ADDITIONAL, db, refresh=False)

    stored_groups = await db.scalars(select(Group.group_number))
    stored_dates = await db.scalars(select(Date.data_value))

    expected_groups = set(GROUPS_INITIAL) | set(GROUPS_ADDITIONAL)
    expected_dates = set(DATES_INITIAL.values()) | set(DATES_ADDITIONAL.values())

    assert set(stored_groups.all()) == expected_groups
    assert set(stored_dates.all()) == expected_dates

    await db.rollback()


@pytest.mark.parametrize(
    "record_index",
    [
        *[record_index 
        for record_index in range(len(CLEANUP_DATES_PAYLOAD))], 
])
@pytest.mark.asyncio(loop_scope="session")
async def test_clean_up_date_removes_matching_record(
    record_index, 
    db: AsyncSession
):
    """Проверяет, что функция clean_up_date удаляет существующую группу"""

    inserted_values = await _seed_dates_for_cleanup(db)
    target_value = inserted_values[record_index]

    response = await clean_up_date(target_value, db)

    remaining = (await db.scalars(select(Date.data_value).order_by(Date.id))).all()
    assert response["status"] == 'ok'
    assert target_value not in remaining


@pytest.mark.asyncio(loop_scope="session")
async def test_clean_up_date_returns_message_when_missing(db: AsyncSession):
    """Проверяет, что функция clean_up_date возвращает error при 
    вводе несуществующей группы"""

    inserted_values = await _seed_dates_for_cleanup(db)

    response = await clean_up_date("not-existed", db)

    remaining = (await db.scalars(select(Date.data_value).order_by(Date.id))).all()
    assert response["status"] == "error"
    assert remaining == inserted_values


@pytest.mark.parametrize(
    "records_amount, expected", 
    [
        *[(record_index, does_not_raise()) 
        for record_index in range(1, len(CLEANUP_DATES_PAYLOAD) + 1)], 
        (len(CLEANUP_DATES_PAYLOAD) + 2, pytest.raises(IndexError)),
])
@pytest.mark.asyncio(loop_scope="session")
async def test_clean_up_dates_deletes_first_n_records(
    records_amount, 
    expected,
    db: AsyncSession,
):  
    """
    Проверяет, что clean_up_dates удаляет первые n записей, если n меньше 
    или равно количества записей в БД и вызывает IndexError, 
    если n больше количества существующих на данный момент в БД записей.
    """

    with expected: 
        inserted_values = await _seed_dates_for_cleanup(db)

        response = await clean_up_dates(records_amount, db)

        remaining = (await db.scalars(select(Date.data_value).order_by(Date.id))).all()
        assert response["status"] == "ok"
        assert remaining == inserted_values[records_amount:]