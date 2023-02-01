import json
from collections import defaultdict, Counter
from itertools import groupby
from operator import itemgetter
from ..utils import get_intersection


def append_duplicates(
    category_check, category, config, duplicates, types, ck
) -> None:
    if category_check["name"] != category["name"]:
        if ck["question"] == config["question"]:
            intersect = get_intersection(ck["options"], config["options"])
            if len(intersect):
                duplicates.append(
                    {
                        "question": ck["question"],
                        "name": category_check["name"],
                        "option": ck["options"],
                        "type": types,
                    }
                )


def loop_duplicates(
    category, config, category_check, duplicates: list
) -> None:
    for types in ["and", "or"]:
        if types in category_check:
            for ck in category_check[types]:
                append_duplicates(
                    category_check=category_check,
                    category=category,
                    config=config,
                    duplicates=duplicates,
                    types=types,
                    ck=ck,
                )


def get_duplicates(category, categories):
    total = 1 if "or" in category else 0
    configs = []
    if "or" in category:
        configs += category["or"]
    else:
        category["or"] = []
    if "and" in category:
        configs += category["and"]
        total += len(category["and"])

    duplicates = []
    for config in configs:
        for category_check in categories:
            loop_duplicates(
                category=category,
                config=config,
                category_check=category_check,
                duplicates=duplicates,
            )
    return configs, duplicates, total


def append_duplicates_dict(duplicate, duplicates, duplicates_dict):
    for types in ["and", "or"]:
        dp = len(
            list(
                filter(
                    lambda x: x["type"] == types
                    and x["name"] == duplicate["name"]
                    and x["question"] == duplicate["question"],
                    duplicates,
                )
            )
        )
        if dp:
            if duplicate["name"] in duplicates_dict:
                if types in duplicates_dict[duplicate["name"]]:
                    duplicates_dict[duplicate["name"]][types] += 1
                else:
                    duplicates_dict[duplicate["name"]][types] = 1
                duplicates_dict[duplicate["name"]]["total"] += 1
            else:
                duplicates_dict[duplicate["name"]] = {
                    "and": 1 if "and" == types else 0,
                    "or": 1 if "or" == types else 0,
                    "total": 1,
                }


def merge_grouped_data(data) -> list:
    merged_data = []
    for key, values in data.items():
        merged = {"name": key}
        for value in values:
            merged.update(value)
        merged_data.append(merged)
    return merged_data


def get_uniq_categories(categories) -> list:
    names = [o["name"] for o in categories]
    dn = [item for item, count in Counter(names).items() if count > 1]
    ld = list(filter(lambda d: d["name"] in dn, categories))
    gd = {
        k: [i for i in g]
        for k, g in groupby(
            sorted(ld, key=itemgetter("name")), key=itemgetter("name")
        )
    }
    mgd = merge_grouped_data(data=gd)
    categories = mgd + list(filter(lambda d: d["name"] not in dn, categories))
    return categories


def get_options(data) -> list:
    options = []
    categories = [c for c in data["categories"]]
    categories = get_uniq_categories(categories=categories)
    for category in categories:
        duplicates_dict = defaultdict()
        configs, duplicates, total = get_duplicates(
            category=category, categories=categories
        )
        for duplicate in duplicates:
            append_duplicates_dict(
                duplicate=duplicate,
                duplicates=duplicates,
                duplicates_dict=duplicates_dict,
            )
        category.update(
            {
                "configs": configs,
                "total": total,
                "duplicates": duplicates,
                "total_duplicate": dict(duplicates_dict),
            }
        )
        options.append(category)
    return options


def loop_options(opt: dict, td: dict, printed: dict, title: str) -> None:
    if opt["total_duplicate"][td]["total"] >= opt["total"]:
        if opt["total_duplicate"][td]["or"] == len(opt["or"]) and opt[
            "total_duplicate"
        ][td]["and"] == len(opt["and"]):
            duplicate = list(
                filter(lambda x: x["name"] == td, opt["duplicates"])
            )
            print(
                f"{title}\n", f"POTENTIAL DUPLICATE: {opt['name']} WITH {td}"
            )
            for d in duplicate:
                print(
                    f"""
                    QUESTION: {d['question']}
                    OPTIONS: {d['option']}
                    """
                )
                printed.update({td: True})


def check_config(file_config) -> bool:
    with open(file_config) as f:
        data = f.read()
        data = json.loads(data)
    counter = 0
    for d in data:
        printed = {}
        options = get_options(data=d)
        for opt in options:
            if opt["name"] in printed:
                continue
            for td in opt["total_duplicate"]:
                loop_options(opt=opt, td=td, printed=printed, title=d["name"])
        if len(printed) > 0:
            counter += 1
            print("===================================================\n")

    return True if counter > 0 else False
