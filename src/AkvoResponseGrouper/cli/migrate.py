import json
import argparse
import re
import os
from enum import Enum
from pydantic import BaseModel, validator
from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import ArgumentError


parser = argparse.ArgumentParser("akvo-responsegrouper")
parser.add_argument(
    "-c",
    "--config",
    help="akvo-responsegrouper -c <json_file_config>",
    type=str,
)
parser.add_argument(
    "-d", "--drop", help="Drop the ar_category view table", action="store_true"
)
args = parser.parse_args()

if args.config:
    print(f"Migrating new config: {args.config}")
elif args.drop:
    print("Drop Table ar_category")
else:
    print(parser.print_help())


class Operator(Enum):
    _or = "or"
    _and = "and"


class CategoryOptions(BaseModel):
    question: int
    options: List[str]


class CategoryBase(BaseModel):
    name: str
    or_: Optional[List[CategoryOptions]] = []
    and_: Optional[List[CategoryOptions]] = []


class CategoryConfigBase(BaseModel):
    name: str
    categories: List[CategoryBase]

    @validator("categories", pre=True, always=True)
    def set_categories(cls, values):
        categories = [
            CategoryBase(
                name=v.get("name"), or_=v.get("or"), and_=v.get("and")
            )
            for v in values
        ]
        return categories


def generate_case(category: CategoryBase, operator: Operator) -> str:
    view_text = ""
    if category:
        for c in category:
            question_id = c.question
            for iop, opt in enumerate(c.options):
                view_text += f"    WHEN ('{opt}' = ANY(options))"
                view_text += f" AND (question = {question_id}) THEN True\n"
                if iop < (len(c.options) - 1):
                    view_text += f"    {operator.value.upper()}\n"
    return view_text


def generate_query(categories: CategoryConfigBase) -> str:
    view_text = ""
    for union, category in enumerate(categories.categories):
        name = category.name
        group = re.sub("[^A-Za-z0-9]+", "_", name).lower()
        valid = len(category.and_) if category.and_ else 0
        valid += 1 if category.or_ else 0
        view_text += f"  SELECT data, COUNT({group}), {valid} as valid,"
        view_text += f" '{name}' as category\n"
        view_text += "  FROM (SELECT data, CASE\n"
        view_text += generate_case(category.and_, Operator._and)
        view_text += generate_case(category.or_, Operator._or)
        view_text += f"    END AS {group}\n"
        view_text += "    FROM\n"
        view_text += "    answer\n"
        view_text += "   ) aw\n"
        view_text += "  WHERE"
        view_text += f" {group} = True\n"
        view_text += "  GROUP BY data\n"
        if union < len(categories.categories) - 1:
            view_text += "  UNION\n"
    return view_text


def drop(engine) -> None:
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
                connection.execute(text("DROP MATERIALIZED VIEW ar_category"))


def check(args):
    DATABASE_URL = os.environ.get("DATABASE_URL")
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
    if args.drop:
        print("Done")
        exit(0)
    return engine


def main():
    engine = check(args)
    file_config = open(args.config)
    config_dict = json.load(file_config)
    file_config.close()

    mview = "CREATE MATERIALIZED VIEW ar_category AS \n"
    for main_union, categories in enumerate(config_dict):
        categories = CategoryConfigBase.parse_raw(json.dumps(categories))
        category_name = categories.name

        mview += "SELECT row_number() over (partition by true) as id,"
        mview += f"data, '{category_name}' as name, category\n"
        mview += "FROM (\n"
        mview += generate_query(categories=categories)
        mview += ") d WHERE d.count = d.valid"
        if main_union < len(config_dict) - 1:
            mview += "\nUNION\n"
        if main_union == len(config_dict) - 1:
            mview += "\nORDER BY data;"

    with engine.connect() as connection:
        with connection.begin():
            connection.execute(text(mview))
    print("Done")


if __name__ == "__main__":
    main()
