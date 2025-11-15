from api.db.database import get_db
from api.db.refresh_db import load_groups_and_dates
from api.routers.users import user_router
from api.parser.group_parser import parse_groups
from api.parser.date_parser import parse_dates
from api.parser.utils import convert_date

from fastapi import FastAPI, Depends, Request, HTTPException, status, Header
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.routers.auth import oauth2_scheme
from sqlalchemy.orm import selectinload
from api.db.models import Group, Date, GroupDateAssociation
import os

# from utils.utils import get_all_dates

app = FastAPI(title="PROGINZH",)

app.mount("/static", StaticFiles(directory="./static"), name="static") # монтируем CSS, js, png etc
templates = Jinja2Templates(directory="templates")


app.include_router(
    user_router,
    prefix="/user",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme)],
)


@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request, db: AsyncSession = Depends(get_db)):
    """Шаблонизатор для приветственной страницы"""

    return templates.TemplateResponse(
        name="index.html", request=request, context={
            'groups': await get_all_groups(db), 
            'dates': await get_all_dates(db),
        }
    )


async def get_all_dates(db: AsyncSession): 
    dates = await db.scalars(select(Date))
    return dates.all()


async def get_all_groups(db: AsyncSession): 
    groups = await db.scalars(select(Group))
    return groups.all()


# Получаем ключ из переменных окружения
API_KEY = os.getenv("ADMIN_API_KEY", 'secret-key')

async def verify_admin_api_key(api_key: str = Header(alias="API-Key")):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )





@app.post("/initial", dependencies=[Depends(verify_admin_api_key)])
async def load_initial_data(db: AsyncSession = Depends(get_db)):
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
    
    dates = [{'date':date.date, "data-value": date.data_value} for date in group.dates]

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
    
    groups = [{'group':group, "data-value": group.data_value} for group in date.groups]

    return {
        "date": date,
        "date_data_value": date.data_value,
        "groups": groups
    }       









