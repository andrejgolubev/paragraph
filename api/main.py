import logging
import uvicorn
from api.settings import settings

from api.db.refresh_db import load_groups_and_dates

from api.db.database import get_db
from api.routers import schedule, homework
from api.auth.users import router as user_router
from api.parser.group_parser import parse_groups
from api.parser.date_parser import parse_dates
from api.parser.utils import convert_date
from api.auth.utils import verify_admin_api_key
from api.db.models import Group, Date

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from api.create_app import create_app


logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)

log = logging.getLogger(__name__)


app = create_app()


app.include_router(user_router)
app.include_router(schedule.schedule_router)
app.include_router(homework.homework_router)


@app.post("/initial", dependencies=[Depends(verify_admin_api_key)])
async def load_initial_groups_and_dates(db: AsyncSession = Depends(get_db)):
    """FOR SUPERUSER ONLY"""
    await load_groups_and_dates(groups=parse_groups(), dates=parse_dates(), db=db)
    return {"status": "Data loaded successfully"}


@app.get('/get-all-dates-related-to-group', dependencies=[Depends(verify_admin_api_key)])
async def get_all_dates_related_to_group(group_number: str, db: AsyncSession = Depends(get_db)):
    """Принимает фактическуюгруппу. FOR SUPERUSER ONLY"""
    group = await db.scalars(select(Group).options(selectinload(Group.dates)).where(Group.group_number == group_number))
    group = group.first()
    
    if not group: 
        raise HTTPException(status_code=404, detail='Group not found or doesn`t exist. Try again or parse relevant data.')
    
    dates = [{'date': date.date, "data-value": date.data_value} for date in group.dates]

    return {
        "group_number": group.group_number,
        "group_data_value": group.data_value,
        "dates": dates
    }   


@app.get('/get-all-groups-related-to-date', dependencies=[Depends(verify_admin_api_key)])
async def get_all_groups_related_to_date(date_input: str, db: AsyncSession = Depends(get_db)):
    """Принимает дату в формате (xx.xx.xxxx) или (xxxx-xx-xx). FOR SUPERUSER ONLY. """
    if '.' in date_input: date_input = convert_date(date_input) 
    date = await db.scalars(select(Date).options(selectinload(Date.groups)).where(Date.data_value == date_input))
    date = date.first()
    if not date: 
        raise HTTPException(status_code=404, detail='Date not found or doesn`t exist. Try again or parse relevant data.')
    
    groups = [{'group': group, "data-value": group.data_value} for group in date.groups]

    return {
        "date": date,
        "date_data_value": date.data_value,
        "groups": groups
    }       

if __name__ == "__main__":
    uvicorn.run(
        app,
        port=8000,
        log_level="info",
        # reload=True
    )
