from api.db.refresh_db import load_groups_and_dates

from api.db.database import get_db
from api.routers import schedule, homework, users, auth
from api.parser.group_parser import parse_groups
from api.parser.date_parser import parse_dates
from api.parser.utils import convert_date
from api.services.data_service import data_service



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

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse



app = FastAPI(title="PROGINZH",)

app.mount("/static", StaticFiles(directory="templates/static"), name="static") # монтируем CSS, js, png etc
templates = Jinja2Templates(directory="templates")


app.include_router(
    users.user_router,
    prefix="/user",
    tags=["users"],
    # dependencies=[Depends(oauth2_scheme)],
)
app.include_router(schedule.schedule_router)
app.include_router(homework.homework_router)





# @app.get("/", response_class=HTMLResponse, name='index')
# async def index_page(request: Request, db: AsyncSession = Depends(get_db)):
#     """Шаблонизатор для приветственной страницы"""
#     groups = await data_service.get_all_groups(db)
#     dates = await data_service.get_all_dates(db)
#     return templates.TemplateResponse( 
#         name="index.html", request=request, context={
#             # 'groups': groups, 
#             # 'dates': dates,
#         }
#     )

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

# Главная страница - отдаем базовый HTML
@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("templates/index.html")





@app.post("/initial", dependencies=[Depends(auth.verify_admin_api_key)])
async def load_initial_groups_and_dates(db: AsyncSession = Depends(get_db)):
    """FOR SUPERUSER ONLY"""
    await load_groups_and_dates(groups=parse_groups(), dates=parse_dates(), db=db)
    return {"status": "Data loaded successfully"}



@app.get('/get-all-dates-related-to-group', dependencies=[Depends(auth.verify_admin_api_key)])
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

    
@app.get('/get-all-groups-related-to-date', dependencies=[Depends(auth.verify_admin_api_key)])
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









