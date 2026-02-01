import json
import pytest
from httpx import ASGITransport, AsyncClient
from asgi_lifespan import LifespanManager

from redis.typing import ResponseT
from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio import Redis
from _pytest.monkeypatch import MonkeyPatch

from backend.api.main import app
from backend.api.routers import schedule as schedule_router_module
from backend.api.db.refresh_db import load_groups_and_dates
from backend.core.config import settings
from backend.tests.conftest import GROUPS_INITIAL


TEST_GROUPS = {
    "5413": "1640",
    "5413М": "1634",
    "5414": "1635",
    "5414": "1635",
    "5415": "1636",
    "5423": "1638",
    "5425": "1646",
}
TEST_DATES = {
    "15.12.2025": "2025-12-15",
    "22.12.2025": "2025-12-22",
    "29.12.2025": "2025-12-29",
    "05.01.2026": "2026-01-05",
    "12.01.2026": "2026-01-12",
    "26.01.2026": "2026-01-19",
    "02.02.2026": "2026-01-26",
}
if (td_len:=len(TEST_DATES)) < (tg_len:=len(TEST_GROUPS)):
    PARAMETRIZE_ITERATIONS_COUNT = range(td_len)
else: 
    PARAMETRIZE_ITERATIONS_COUNT = range(tg_len)


class ParseScheduleStub:
    """
    Класс-заглушка, экземпляр которого подменяет функцию parse_schedule_from_url. 
    Метод __call__ позволяет понять, что будет возвращать парсер и посмотреть, 
    сколько раз он вызвалcя.
    """

    def __init__(self):
        self.call_count = 0

    async def __call__(self, *args, **kwargs):
        """
        self.call_count инкрементируется каждый раз, когда вызывается 
        parse_schedule_from_url, здесь увеличивается self.call_count, 
        что позволяет понять, сколько раз парсер действительно запускался. 

        Возвращает {"from_stub": True} , сигнализирующий о вызове 
        именно заглушки, а не реальной функции parse_schedule_from_url 
        """
        self.call_count += 1
        return {"from_stub": True}


@pytest.fixture
async def ensure_schedule_data(db: AsyncSession):
    await load_groups_and_dates(GROUPS_INITIAL, TEST_DATES, db, refresh=False)
    await load_groups_and_dates(TEST_GROUPS, TEST_DATES, db, refresh=False)
    yield


@pytest.fixture
async def redis_client():
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        password=settings.redis.password,
        db=settings.redis.db,
    )
    # smoke-check connection
    await redis.ping()
    yield redis
    await redis.aclose()

@pytest.mark.parametrize(
    "index", 
    [*[ind for ind in PARAMETRIZE_ITERATIONS_COUNT]]
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_schedule_caches_response(
    monkeypatch: MonkeyPatch,
    redis_client: Redis,
    index: int
):
    """
    Проверяет, кэшируется ли расписание при совершенных подряд 
    вызовах эндпоинта get_schedule с идентичными данными. 
    Проверка основывается на том, была ли вызвана ф-ция parse_schedule_from_url: 
    если была, значит расписание закешировано не было, если не была - значит было.
    Отследить кол-во вызовов помогает метод __call__ класса ParseScheduleStub.
    """
    
    parse_stub = ParseScheduleStub()
    monkeypatch.setattr(
        schedule_router_module, "parse_schedule_from_url", parse_stub
    )
    params = {
        "group_data_value": list(TEST_GROUPS.values())[index],
        "date_data_value": list(TEST_DATES.values())[index],
    }
    cache_key = schedule_router_module._build_cache_key(
        params["group_data_value"], params["date_data_value"]
    )
    await redis_client.delete(cache_key)

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app), 
            base_url="http://test", 
        ) as client:
            first = await client.get("/schedule/get-schedule", params=params)
            second = await client.get("/schedule/get-schedule", params=params)


    assert first.status_code == 200
    assert second.status_code == 200

    assert first.json() == {"from_stub": True}
    assert second.json() == {"from_stub": True}
    
    # проверяем, что расписание берется уже из кэша на втором идентичном запросе
    assert parse_stub.call_count == 1

    cached: ResponseT = await redis_client.get(cache_key)
    assert cached is not None
    assert cached.decode() == json.dumps({"from_stub": True})


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_groups_and_dates(ensure_schedule_data):
    """Проверяет работу эндпоинтов get_all_groups и get_all_dates"""
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app), 
            base_url="http://test", 
        ) as client:
            groups_resp = await client.get("/schedule/get-all-groups")
            dates_resp = await client.get("/schedule/get-all-dates")


    assert groups_resp.status_code == 200
    assert [group["group_number"] == TEST_GROUPS.keys() for group in groups_resp.json()]
    assert [group["data_value"] == TEST_GROUPS.values() for group in groups_resp.json()]

    assert dates_resp.status_code == 200
    assert [date["date"] == TEST_DATES.keys() for date in dates_resp.json()]
    assert [date["data_value"] == TEST_DATES.values() for date in dates_resp.json()]