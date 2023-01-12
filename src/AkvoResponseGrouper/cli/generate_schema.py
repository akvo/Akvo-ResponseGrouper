import json
import re
from enum import Enum
from pydantic import BaseModel, validator
from typing import Optional, List


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
    if not category:
        return ""
    for i, c in enumerate(category):
        last = i == len(category) - 1
        question_id = c.question
        opt = ", ".join([f"'{op}'" for op in c.options])
        opt = f"ANY(ARRAY[{opt}])"
        if operator == Operator._and or not i:
            view_text += "    WHEN"
        if operator == Operator._or:
            view_text += " \n    (CASE WHEN "
        view_text += f" ((opt = {opt})"
        view_text += f" AND (question = {question_id}))"
        if operator == Operator._or:
            view_text += " THEN True END)"
        if operator == Operator._and:
            view_text += " THEN True\n"
        if operator == Operator._or and not last:
            view_text += " OR\n"
        if operator == Operator._or and last:
            view_text += " THEN True\n"
    return view_text


def generate_query(categories: CategoryConfigBase) -> str:
    view_text = ""
    for union, category in enumerate(categories.categories):
        name = category.name
        group = re.sub("[^A-Za-z0-9]+", "_", name).lower()
        valid = len(category.and_) if category.and_ else 0
        valid += 1 if category.or_ else 0
        view_text += "  SELECT form, data"
        view_text += f", COUNT({group}), {valid} as valid,"
        view_text += f" '{name}' as category\n"
        view_text += "  FROM (SELECT form, data, CASE\n"
        view_text += generate_case(category.and_, Operator._and)
        view_text += generate_case(category.or_, Operator._or)
        view_text += f"    END AS {group}\n"
        view_text += "    FROM\n"
        view_text += "    (SELECT\n"
        view_text += "     q.form, aa.data"
        view_text += ", aa.question, unnest(aa.options)::TEXT as opt\n"
        view_text += "     FROM answer aa\n"
        view_text += "     LEFT JOIN question q ON q.id = aa.question) a\n"
        view_text += "   ) aw\n"
        view_text += "  WHERE"
        view_text += f" {group} = True\n"
        view_text += "  GROUP BY data, form\n"
        if union < len(categories.categories) - 1:
            view_text += "  UNION\n"
    return view_text


def generate_schema(file_config: str) -> str:
    file_config = open(file_config)
    config_dict = json.load(file_config)
    file_config.close()
    mview = "CREATE MATERIALIZED VIEW ar_category AS \n"
    for main_union, categories in enumerate(config_dict):
        categories = CategoryConfigBase.parse_raw(json.dumps(categories))
        category_name = categories.name

        mview += "SELECT row_number() over (partition by true) as id,"
        mview += f"form, data, '{category_name}' as name, category\n"
        mview += "FROM (\n"
        mview += generate_query(categories=categories)
        mview += ") d WHERE d.count >= d.valid"
        if main_union < len(config_dict) - 1:
            mview += "\nUNION\n"
        if main_union == len(config_dict) - 1:
            mview += "\nORDER BY data;"
    return mview
