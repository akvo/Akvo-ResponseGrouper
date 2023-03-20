import json


def check_config(file_config: str, info: bool = True) -> int:
    with open(file_config) as f:
        data = f.read()
        data = json.loads(data)
    counter = 0
    for d in data:
        printed = {}
        for opt in d:
            if opt["name"] in printed:
                continue
        if len(printed) > 0:
            counter += len(printed)
    return counter
