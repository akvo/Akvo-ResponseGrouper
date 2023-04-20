import json
import pandas as pd
from itertools import groupby


def get_category_key(k: dict):
    return k["name"]


def group_by_category_output(data):
    g = sorted(data, key=get_category_key)
    res = [
        {
            "category": key[0],
            "form": key[1],
            "options": [
                {"name": o["category"], "count": o["count"]}
                for o in list(value)
            ],
        }
        for key, value in groupby(g, key=lambda x: (x["name"], x["form"]))
    ]
    return res


def flatten_list(ld: list) -> list:
    return [item for sublist in ld for item in sublist]


def get_intersection(lst1, lst2) -> list:
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def generate_data_as_json_file(data: list):
    # Serializing json
    json_object = json.dumps(data, indent=4)
    # Writing to test.json
    with open("test.json", "w") as outfile:
        outfile.write(json_object)
    return "test.json"


def validate_number(q, answer):
    aw = float(answer[0])
    op = q.get("number")
    ok = False
    if "greater_than" in op:
        ok = aw > op.get("greater_than")
    if "less_than" in op:
        ok = aw < op.get("less_than")
    if "equal" in op:
        ok = aw == op.get("equal")
    if "greater_than_equal" in op:
        ok = aw >= op.get("greater_than_equal")
    if "less_than_equal" in op:
        ok = aw <= op.get("less_than_equal")
    return ok


def get_valid_list(opt, c, category):
    validator = [q["id"] for q in c["questions"]]
    valid = []
    exit = False
    for q in c["questions"]:
        if exit:
            continue
        answer = opt.get(str(q["id"]))
        if not answer:
            opt.update({str(q["id"]): None})
            continue
        if q.get("number"):
            is_valid = validate_number(q, answer)
            if is_valid:
                valid.append(q["id"])
            else:
                elses = q.get("else")
                category = elses.get("name")
                exit = True
        if q.get("options"):
            if len(set(q["options"]).intersection(answer)):
                valid.append(q["id"])
            # TODO Merge else with above
            else:
                if q.get("else"):
                    elses = q.get("else")
                    if elses.get("name"):
                        category = elses.get("name")
                        exit = True
                    if elses.get("ignore"):
                        validator = list(
                            filter(
                                lambda x: x not in elses.get("ignore"),
                                validator,
                            )
                        )
                        valid.append(q["id"])
                if q.get("other"):
                    for o in q.get("other"):
                        if len(set(o["options"]).intersection(answer)):
                            exit = True
                            if len(o.get("questions")):
                                category = get_valid_list(opt, o, category)
                            else:
                                category = o.get("name")
    if len(valid) > len(validator):
        conditions = [v if v in valid else False for v in validator]
        conditions = list(filter(lambda x: x is not False, conditions))
        if sorted(conditions) == sorted(validator):
            category = c["name"]
    if sorted(valid) == sorted(validator):
        category = c["name"]
    return category


def get_category(opt: dict, file_path: str = "./.category.json"):
    with open(f"{file_path}") as config_file:
        configs = json.load(config_file)
    category = False
    for config in configs:
        for c in config["categories"]:
            category = get_valid_list(opt, c, category)
    return category


def transform_categories_to_df(
    categories: list, file_path: str = "./.category.json"
):
    df = pd.DataFrame(categories)
    results = df.to_dict("records")
    for d in results:
        d.update({"category": get_category(opt=d["opt"], file_path=file_path)})
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


def get_counted_category(df):
    return (
        df.groupby(["name", "category", "form"])["category"]
        .agg("count")
        .reset_index(name="count")
    ).to_dict("records")
