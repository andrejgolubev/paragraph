from fastapi import Response, HTTPException, APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from backend.api.db.database import get_db
from backend.api.parser.schedule_parser import parse_schedule_from_url, parse_schedule  
from sqlalchemy.ext.asyncio import AsyncSession
from backend.api.services.data_service import data_service
from backend.api.core.config import settings

from redis.asyncio import Redis
import json

router = schedule_router = APIRouter(tags=['schedule'], prefix='/schedule')


def _build_cache_key(group_data_value: str | None, date_data_value: str | None) -> str:
    group_dv = group_data_value or "default"
    date_dv = date_data_value or "current"
    return f"schedule:{group_dv}:{date_dv}"


@router.get("/get-schedule")
async def get_schedule(
    request: Request,
    group_data_value: str | None = None,
    date_data_value: str | None = None,
):
    url = (
        f"https://rasp.rsreu.ru/schedule-frame/group?faculty=1"
        f"&group={group_data_value}&date={date_data_value or ''}"
    )

    redis_client: Redis | None = getattr(request.app.state, "redis", None)
    cache_key = _build_cache_key(group_data_value, date_data_value)
    if redis_client:
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

    try:
        schedule_data = await parse_schedule_from_url(url, function=parse_schedule)
        if redis_client:
            await redis_client.set(
                cache_key, 
                json.dumps(schedule_data), 
                ex=settings.redis.schedule_cache_ttl
            )
        return schedule_data
    except Exception:
        raise HTTPException(status_code=500, detail=f"Error parsing schedule.")


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