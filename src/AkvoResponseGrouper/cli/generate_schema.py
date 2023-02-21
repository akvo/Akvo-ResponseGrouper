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


def get_question_config(config: dict, cl: list):
    for q in config.get("questions"):
        cl.append(str(q["id"]))
        if q.get("other"):
            for o in q.get("other"):
                cl = get_question_config(config=o, cl=cl)
    return cl


def generate_schema(file_config: str) -> str:
    file_config = open(file_config)
    configs = json.load(file_config)
    file_config.close()
    mview = "CREATE MATERIALIZED VIEW ar_category AS \n"
    mview += "SELECT *, row_number() over (partition by true) as id FROM ("
    for main_union, config in enumerate(configs):
        question_config = []
        for c in config["categories"]:
            question_config = get_question_config(config=c, cl=question_config)
        ql = ",".join(question_config)
        mview += (
            f"SELECT q.form, a.data, '{config['name']}' as name,"
            " jsonb_object_agg(a.question,COALESCE(a.options,"
            " array[a.value::text])) as opt \n"
        )
        mview += "FROM answer a \n"
        mview += "LEFT JOIN question q ON q.id = a.question \n"
        mview += "WHERE (a.value IS NOT NULL OR a.options IS NOT NULL) \n"
        mview += f"AND q.id IN ({ql}) GROUP BY q.form, a.data\n"
        if main_union < len(configs) - 1:
            mview += " UNION "
    mview += ") as categories;"
    return mview
