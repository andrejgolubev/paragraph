"""CLI entrypoint to refresh groups and dates outside of FastAPI."""
import argparse
import asyncio

from ..db.refresh_db import load_groups_and_dates
from ..db.database import AsyncSessionLocal
from ..parser.group_parser import parse_groups
from ..parser.date_parser import parse_dates


async def _reload_db(refresh: bool) -> None:
    groups = parse_groups()
    dates = parse_dates()
    async with AsyncSessionLocal() as session:
        await load_groups_and_dates(groups=groups, dates=dates, db=session, refresh=refresh)


def main():
    parser = argparse.ArgumentParser(
        prog="reload_db",
        description="Парсит группы и даты вручную."
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="Очистить базу перед загрузкой."
    )
    args = parser.parse_args()

    asyncio.run(_reload_db(refresh=args.refresh))


if __name__ == "__main__":
    main()

