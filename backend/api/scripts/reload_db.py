"""CLI entrypoint для загрузки и обновления групп и дат в БД """
import argparse
import asyncio

from ..db.refresh_db import load_groups_and_dates
from ..db.database import AsyncSessionLocal, AsyncSessionLocalTest
from ..parser.group_parser import parse_groups
from ..parser.date_parser import parse_dates


async def _reload_db(refresh: bool, test: bool) -> None:
    groups = parse_groups()
    dates = parse_dates()
    if test:
        db = AsyncSessionLocalTest()
    else:
        db = AsyncSessionLocal()
    async with db as session:
        await load_groups_and_dates(groups=groups, dates=dates, db=session, refresh=refresh)


def main():
    parser = argparse.ArgumentParser(
        prog="reload_db",
        description="Парсит группы и даты вручную."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Укажите, чтобы очистить базу перед загрузкой."
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Укажите, чтобы использовать тестовую БД."
    )
    args = parser.parse_args()

    asyncio.run(_reload_db(
        refresh=args.refresh,
        test=args.test
    ))



if __name__ == "__main__":
    main()

