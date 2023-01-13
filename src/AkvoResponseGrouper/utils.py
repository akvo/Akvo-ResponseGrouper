from itertools import groupby


def key_func(k):
    return k["name"]


def grouped_items(data):
    g = sorted(data, key=key_func)
    return [
        {
            "category": key,
            "options": [
                {"name": o.category, "count": o.count} for o in list(value)
            ],
        }
        for key, value in groupby(g, key_func)
    ]
