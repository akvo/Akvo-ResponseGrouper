import json
import pandas as pd
from typing import List, Optional
from sqlalchemy.orm import Session
from .models import Category, CategoryDict
from .utils import get_valid_list


def get_category(opt: dict):
    file_path = "./.category.json"
    with open(f"{file_path}") as config_file:
        configs = json.load(config_file)
    category = False
    for config in configs:
        for c in config["categories"]:
            category = get_valid_list(opt, c, category)
    return category


def get_data_categories(session: Session):
    categories = session.query(Category).all()
    categories = [c.serialize for c in categories]
    return categories


def get_results(session: Session):
    categories = get_data_categories(session=session)
    df = pd.DataFrame(categories)
    results = df.to_dict("records")
    for d in results:
        d.update({"category": get_category(d["opt"])})
    res = pd.DataFrame(results)
    if list(res) != ["id", "data", "form", "name", "opt", "category"]:
        return pd.DataFrame(
            columns=[
                "id",
                "data",
                "form",
                "name",
                "category",
            ]
        )
    res = pd.concat(
        [res.drop("opt", axis=1), pd.DataFrame(df["opt"].tolist())], axis=1
    )
    return res[
        [
            "id",
            "data",
            "form",
            "name",
            "category",
        ]
    ]


def get_categories(
    session: Session,
    form: Optional[int] = None,
    name: Optional[str] = None,
    category: Optional[str] = None,
    data: Optional[str] = None,
) -> List[CategoryDict]:
    res = get_results(session=session)
    queries = []
    if form:
        queries.append(f"form == {form}")
    if name:
        queries.append(f"name.str.lower() == '{name.lower()}'")
    if category:
        queries.append(f"category.str.lower() == '{category.lower()}'")
    if data:
        data = [int(d) for d in data.split(",")]
        queries.append("data.isin(@data).values")
    if len(queries):
        queries = " & ".join(queries)
        res = res.query(queries)
    return res.to_dict("records")


def get_group_by_category(
    session: Session,
    category: Optional[str] = None,
    form: Optional[int] = None,
):
    res = get_results(session=session)
    queries = []
    if form:
        queries.append(f"form == {form}")
    if category:
        queries.append(f"category.str.lower() == '{category.lower()}'")
    if len(queries):
        queries = " & ".join(queries)
        res = res.query(queries)
    res = (
        res.groupby(["name", "category"])["category"]
        .agg("count")
        .reset_index(name="count")
    )
    return res.to_dict("records")


def refresh_view(session: Session):
    session.execute("REFRESH MATERIALIZED VIEW ar_category;")
    session.commit()
