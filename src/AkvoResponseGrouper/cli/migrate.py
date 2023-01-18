import argparse
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import ArgumentError
from .generate_schema import generate_schema


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
args = parser.parse_args()

if not args.config and not args.refresh:
    parser.print_help()
    exit(0)

if args.config and args.refresh:
    parser.print_help()
    exit(0)

if args.config:
    print(f"Migrating new config: {args.config}")
if args.refresh:
    print("Refresh Table ar_category")


def refresh(engine) -> None:
    with engine.connect() as connection:
        with connection.begin():
            existing_view = connection.execute(
                text(
                    """
                SELECT count(relkind) from pg_class
                where relname = 'ar_category'
                and relkind = 'm'
                """
                )
            ).fetchone()
            if existing_view["count"]:
                connection.execute(
                    text("REFRESH MATERIALIZED VIEW ar_category")
                )


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

    if args.refresh or args.config:
        refresh(engine)
    if args.refresh:
        print("Done")
        exit(0)
    return engine


def main() -> None:
    engine = check()
    schema = generate_schema(file_config=args.config)
    with engine.connect() as connection:
        with connection.begin():
            connection.execute(text(schema))
    print("Done")


if __name__ == "__main__":
    main()
