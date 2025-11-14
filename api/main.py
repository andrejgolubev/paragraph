from fastapi import FastAPI, Depends, Request
from api.routers.users import user_router
from api.auth import oauth2_scheme
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title="PROGINZH",)

# монтируем CSS, js, png etc
# app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="templates")
# create the instance for the routes

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
            
        }
    )


@app.get(path='/schedule/{group_number}', )







