import json
import numpy as np
import pandas as pd
from AkvoResponseGrouper.utils import (
    get_category,
)


with open("./check/category.json", "r") as category_json:
    categories = json.loads(category_json.read())


data = pd.read_csv("./check/2018_data_export_new.csv")

# Remove columns containing '--other--' or '--OTHER--'
columns_to_remove = [col for col in data.columns if '--other--' in col.lower()]
data.drop(columns=columns_to_remove, inplace=True)
# Create an auto-incremented ID column
data['id'] = np.arange(len(data)) + 1

# save data without other
pd.DataFrame(data).to_csv("./check/siwins-2018-data-without-other-new.csv", index=None)

col_names = {d: d.split("|")[0] for d in list(data)}
data = data.rename(columns=col_names)


meta = ['id',
        'Identifier',
        'Display Name',
        'Device identifier',
        'Submitter',
        'Form version']


question_ids = []
for category in categories:
    for ct in category['categories']:
        questions = ct.get('questions', [])
        for question in questions:
            question_ids.append(str(question['id']))


data = data[meta + list(set(question_ids))]


def split_value(value):
    if type(value) == str:
        if ":" in value:
            return [v.split(":")[1].strip() if ":" in v else v.strip() for v in value.split("|")]
        return [v.strip() for v in value]
    return []


for column in list(set(question_ids)):
    data[str(column)] = data[column].apply(lambda x: split_value(x))


results = []
for d in data.to_dict("records"):
    answers = {}
    result = {"id": d["id"]}
    for col in list(set(question_ids)):
        answers.update({col: d[col]})
    for category in categories:
        res = {
            "id": d["id"],
            "data": d["id"],
            "opt": answers,
            "name": category["name"]
        }
        ct = get_category(data=res)
        result.update({category["name"]: ct})
    results.append(result)


pd.DataFrame(results).to_csv("./check/results-siwins-2018-data-without-other.csv", index=None)
