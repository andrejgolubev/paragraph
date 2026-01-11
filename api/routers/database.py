from api.db.refresh_db import cleanup_dates_by_period, load_groups_and_dates

from api.db.database import get_db
from api.parser.group_parser import parse_groups
from api.parser.date_parser import parse_dates
from api.parser.utils import convert_date
from api.auth.utils import verify_admin_api_key
from api.db.models import Group, Date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

router = database_router = APIRouter(tags=['Database'], prefix='/database')

@router.post("/initial", dependencies=[Depends(verify_admin_api_key)])
async def load_initial_groups_and_dates(
    refresh: bool = Query(False, description="полностью обновить базу данных?"), 
    db: AsyncSession = Depends(get_db)
):
    """Начальная загрузка групп и дат в базу данных."""
    await load_groups_and_dates(groups=parse_groups(), dates=parse_dates(), db=db, refresh=refresh)
    return {"status": "Data loaded successfully"}


@router.post("/cleanup-dates", dependencies=[Depends(verify_admin_api_key)])
async def cleanup_dates(
    start_date: str | None = Query(None, description="Начальная дата (dd.mm.yyyy или yyyy-mm-dd)"), 
    end_date: str | None = Query(None, description="Конечная дата (dd.mm.yyyy или yyyy-mm-dd)"), 
    db: AsyncSession = Depends(get_db)
):
    """Очистка дат в базу данных за указанный период."""
    return await cleanup_dates_by_period(start_date=start_date, end_date=end_date, db=db)


@router.get('/get-all-dates-related-to-group', dependencies=[Depends(verify_admin_api_key)])
async def get_all_dates_related_to_group(
    group_number: str = Query(..., description="Фактическая группа"), 
    db: AsyncSession = Depends(get_db)
):
    """Получение всех дат, связанных с группой."""
    group_result = await db.scalars(select(Group).options(selectinload(Group.dates)).where(Group.group_number == group_number))
    group = group_result.first()
    
    if not group: 
        raise HTTPException(status_code=404, detail='Group not found or doesn`t exist.')
    
    dates = [{'date': date.date, "data-value": date.data_value} for date in group.dates]

    return {
        "group_number": group.group_number,
        "group_data_value": group.data_value,
        "dates": dates
    }   


@router.get('/get-all-groups-related-to-date', dependencies=[Depends(verify_admin_api_key)])
async def get_all_groups_related_to_date(
    date_input: str = Query(..., description="Дата (dd.mm.yyyy или yyyy-mm-dd)"), 
    db: AsyncSession = Depends(get_db)
):
    """Получение всех групп, связанных с датой."""
    if '.' in date_input: date_input = convert_date(date_input) 
    date_result = await db.scalars(select(Date).options(selectinload(Date.groups)).where(Date.data_value == date_input))
    date = date_result.first()
    if not date: 
        raise HTTPException(status_code=404, detail='Date not found or doesn`t exist.')
    
    groups = [{'group': group, "data-value": group.data_value} for group in date.groups]

    return {
        "date": date,
        "date_data_value": date.data_value,
        "groups": groups
    }   