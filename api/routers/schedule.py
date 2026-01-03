from fastapi import Request, Response, HTTPException, APIRouter, Depends
from fastapi.responses import JSONResponse
from api.db.database import get_db
from api.parser.schedule_parser import parse_schedule_from_url, parse_schedule  
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.schemas import GroupSelection
from api.services.data_service import data_service
from api.settings import settings

router = schedule_router = APIRouter(tags=['Schedule'], prefix='/schedule')


@router.get("/get-schedule")
async def get_schedule(
    response: Response,
    group_data_value: str | None = None,
    date_data_value: str | None = None,
):
        
    url = f'https://rasp.rsreu.ru/schedule-frame/group?faculty=1&group={group_data_value}&date={date_data_value or ""}'    

    

    try:    
        schedule_data = await parse_schedule_from_url(url, function=parse_schedule) 
        return schedule_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing schedule: {str(e)}")




@router.post("/select-group")
async def select_group(
    group_data: GroupSelection,
    response: Response,
):
    # Сохраняем в cookie на 30 дней
    response.set_cookie(
        key="selected_group",
        value=group_data.group_data_value,
        max_age=30*24*60*60,  # 30 дней
        httponly=True,
        samesite='none', # обязательно 'lax' для продакшна
        secure=True  
    )
    
    return {"status": "success", "selected_group": group_data.group_data_value} 



@router.get('/get-all-groups', response_class=JSONResponse)
async def get_all_groups(db: AsyncSession = Depends(get_db)): 
    return await data_service.get_all_groups(db)


@router.get('/get-all-dates', response_class=JSONResponse)
async def get_all_dates(db: AsyncSession = Depends(get_db)): 
    dates = await data_service.get_all_dates(db) 
    return [
        {
            "date": date.date,
            'data_value': date.data_value,
        }
        for date in dates
    ]