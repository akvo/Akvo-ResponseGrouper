import json
from itertools import groupby


def get_category_key(k):
    return k["name"]


def group_by_category_output(data):
    g = sorted(data, key=get_category_key)
    return [
        {
            "category": key,
            "options": [
                {"name": o["category"], "count": o["count"]}
                for o in list(value)
            ],
        }
        for key, value in groupby(g, get_category_key)
    ]


def flatten_list(ld: list) -> list:
    return [item for sublist in ld for item in sublist]


def get_intersection(lst1, lst2) -> list:
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


def get_list_questions(data: list) -> list:
    categories = [d["categories"] for d in data]
    categories = flatten_list(ld=categories)
    lq = []
    for c in categories:
        if "or" in c:
            lq += c["or"]
        if "and" in c:
            lq += c["and"]
    return lq


def get_total_criteria_per_category(category: dict) -> int:
    total = 1 if "or" in category else 0
    if "and" in category:
        total += len(category["and"])
    return total


def generate_data_as_json_file(data: list):
    # Serializing json
    json_object = json.dumps(data, indent=4)
    # Writing to test.json
    with open("test.json", "w") as outfile:
        outfile.write(json_object)
    return "test.json"
