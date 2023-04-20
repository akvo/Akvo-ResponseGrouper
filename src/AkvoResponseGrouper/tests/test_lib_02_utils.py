import os
import pandas as pd
from ..utils import (
    group_by_category_output,
    get_intersection,
    generate_data_as_json_file,
    get_valid_list,
    flatten_list,
    validate_number,
    get_counted_category,
)

"""
A test case for utils with pytest
"""


def test_transform_array():
    fake_array = [
        {"category": "Basic", "name": "Category 1", "count": 10, "form": 1},
        {"category": "Limited", "name": "Category 1", "count": 15, "form": 1},
    ]
    assert group_by_category_output(fake_array) == [
        {
            "category": "Category 1",
            "form": 1,
            "options": [
                {
                    "name": "Basic",
                    "count": 10,
                },
                {
                    "name": "Limited",
                    "count": 15,
                },
            ],
        }
    ]


def test_list_get_intersection():
    lst1 = [1, 2]
    lst2 = [2, 3, 4]
    li = get_intersection(lst1, lst2)
    assert li == [2]


def test_generated_data_exists():
    fake_data = [1, 2, 3]
    PATH = generate_data_as_json_file(data=fake_data)
    assert True if os.path.isfile(PATH) else False


def test_get_valid_list():
    opt = {
        "567820002": ["Yes"],
        "567800083": ["No"],
        "578820191": ["Girls Only"],
    }
    c = {
        "name": "Basic",
        "questions": [
            {
                "id": 567820002,
                "name": "Toilet Available?",
                "options": ["Yes"],
                "else": {
                    "name": "No Service",
                    "ignore": [567800083, 578820191],
                },
            },
            {
                "id": 567800083,
                "name": "Share with outside member?",
                "options": ["No"],
                "else": {"name": "Limited"},
            },
            {
                "id": 578820191,
                "name": "A",
                "options": ["Boys n Girls"],
                "other": [
                    {
                        "name": "Limited",
                        "options": ["Girls Only", "Boys Only"],
                        "questions": [],
                    }
                ],
                "else": {"name": "No facility"},
            },
        ],
    }
    category = False
    _category = get_valid_list(opt, c, category)
    assert _category == "Limited"
    opt2 = {
        "567820002": ["No"],
    }
    _category2 = get_valid_list(opt2, c, category)
    assert _category2 == "Basic"


def test_get_flatten_list():
    list = [[1, 2, 3], [4, 5, 6]]
    results = flatten_list(ld=list)
    assert results == [1, 2, 3, 4, 5, 6]


def test_valid_number():
    answer = [10]
    opt1 = {"number": {"greater_than": 0}}
    res1 = validate_number(q=opt1, answer=answer)
    assert res1 is True

    opt2 = {"number": {"less_than": 11}}
    res2 = validate_number(q=opt2, answer=answer)
    assert res2 is True

    opt3 = {"number": {"equal": 10}}
    res3 = validate_number(q=opt3, answer=answer)
    assert res3 is True

    opt4 = {"number": {"greater_than_equal": 10}}
    res4 = validate_number(q=opt4, answer=answer)
    assert res4 is True

    opt5 = {"number": {"less_than_equal": 10}}
    res5 = validate_number(q=opt5, answer=answer)
    assert res5 is True


def test_get_counted_category():
    categories = [
        {
            "id": 1,
            "data": 1,
            "form": 1,
            "name": "Water",
            "category": "Limited",
        },
        {
            "id": 1,
            "data": 2,
            "form": 1,
            "name": "Water",
            "category": "Basic",
        },
    ]
    df = pd.DataFrame(categories)
    grouped = get_counted_category(df=df)
    assert grouped == [
        {"category": "Basic", "count": 1, "form": 1, "name": "Water"},
        {"category": "Limited", "count": 1, "form": 1, "name": "Water"},
    ]
