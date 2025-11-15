from fastapi import FastAPI, Depends, Request, HTTPException, status, Header
from api.routers.users import user_router
from api.routers.auth import oauth2_scheme
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.database import get_db
from api.db.refresh_db import load_groups_and_dates
from api.parser.group_parser import parse_groups
from api.parser.date_parser import parse_dates
from sqlalchemy import select
from api.db.models import Group, Date, GroupDateAssociation
import os

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
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html", request=request, context={
            'hello': 'hi'
        }
    )





# Получаем ключ из переменных окружения
API_KEY = os.getenv("ADMIN_API_KEY", 'secret-key')

async def verify_admin_api_key(api_key: str = Header(alias="X-API-Key")):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )

@app.post("/initial", dependencies=[Depends(verify_admin_api_key)])




@app.post("/initial", dependencies=[Depends(verify_admin_api_key)])
async def load_initial_data(db: AsyncSession = Depends(get_db)):
    """FOR SUPERUSER (ME) ONLY"""
    await load_groups_and_dates(groups=parse_groups(), dates=parse_dates(), db=db)
    return {"status": "Data loaded successfully"}


# @app.post('/getsmh')
# async def get_all_dates_related_to_group(group_number: str, db: AsyncSession = Depends(get_db)):
#     group = await db.scalars(select(Group).where(Group.group_number == group_number))
#     group_id = group.first().id 
#     date_scalars = await db.scalars(select(GroupDateAssociation).where(GroupDateAssociation.group_id == group_id))
#     date_id = date_scalars.first().id #type:ignore 
#     stmt = await db.scalars(select(Date).where(Date.id == date_id))
#     return stmt.first().date #type:ignore 
    

    
    








