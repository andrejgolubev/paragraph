from fastapi import FastAPI, Depends, Request
from api.routers.users import user_router
from api.routers.auth import oauth2_scheme
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from api.routers.schedule import schedule_router
from api.db.database import get_db
from api.routers.schedule import load_groups_and_dates
from api.parser.group_parser import parse_groups
from api.parser.date_parser import parse_dates


app = FastAPI(title="PROGINZH",)

app.mount("/static", StaticFiles(directory="./static"), name="static") # монтируем CSS, js, png etc
templates = Jinja2Templates(directory="templates")


app.include_router(
    user_router,
    prefix="/user",
    tags=["users"],
    dependencies=[Depends(oauth2_scheme)],
)

app.include_router(schedule_router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html", request=request, context={
            'hello': 'hi'
        }
    )


@app.post("/initial")
async def load_initial_data(db: AsyncSession = Depends(get_db)):
    await load_groups_and_dates(groups=parse_groups(), dates=parse_dates(), db=db)
    return {"status": "Data loaded successfully"}









