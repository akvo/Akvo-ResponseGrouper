import argparse
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import ArgumentError
from .generate_schema import generate_schema
from ..db import get_existing_view, drop_view

parser = argparse.ArgumentParser("akvo-responsegrouper")
parser.add_argument(
    "-c",
    "--config",
    help="akvo-responsegrouper -c <json_file_config>",
    type=str,
)
parser.add_argument(
    "-d",
    "--database",
    help="akvo-responsegrouper -d <DATABASE_URL>",
    type=str,
)
parser.add_argument(
    "-r",
    "--refresh",
    help="Refresh the ar_category view table",
    action="store_true",
)
parser.add_argument(
    "-dv",
    "--drop",
    help="Drop the ar_category view table",
    action="store_true",
)
args = parser.parse_args()

if (
    not args.config
    and not args.refresh
    and not args.drop
    and not args.database
):
    parser.print_help()
    exit(0)

if args.config and args.drop:
    parser.print_help()
    exit(0)

if args.config:
    print(f"Migrating new config: {args.config}")
if args.refresh:
    print("Refresh View ar_category")
if args.drop:
    print("Drop View ar_category")


def refresh(engine) -> None:
    with engine.connect() as connection:
        with connection.begin():
            existing_view = get_existing_view(connection)
            if existing_view["count"]:
                connection.execute(
                    text("REFRESH MATERIALIZED VIEW ar_category")
                )


def drop(engine) -> None:
    with engine.connect() as connection:
        with connection.begin():
            existing_view = get_existing_view(connection)
            if existing_view["count"]:
                drop_view(connection)


def get_db_url() -> str:
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if args.database:
        DATABASE_URL = args.database
    return DATABASE_URL


def check():
    DATABASE_URL = get_db_url()
    if not DATABASE_URL:
        print("DATABASE_URL variable not found")
        exit(1)

    try:
        engine = create_engine(DATABASE_URL)
    except ArgumentError:
        print(f"Error connection from {DATABASE_URL}")
        exit(1)

    if args.drop or args.config:
        drop(engine)
    if args.refresh:
        refresh(engine)
        print("Done")
        exit(0)
    return engine


def main() -> None:
    engine = check()
    if args.config:
        schema = generate_schema(file_config=args.config)
        with engine.connect() as connection:
            with connection.begin():
                connection.execute(text(schema))
    print("Done")


if __name__ == "__main__":
    main()
