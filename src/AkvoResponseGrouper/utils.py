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
