import os
from ..utils import (
    group_by_category_output,
    get_list_questions,
    get_intersection,
    generate_data_as_json_file,
    get_total_criteria_per_category,
)

"""
A test case for utils with pytest
"""


def test_transform_array():
    fake_array = [
        {"category": "Basic", "name": "Category 1", "count": 10},
        {"category": "Limited", "name": "Category 1", "count": 15},
    ]
    assert group_by_category_output(fake_array) == [
        {
            "category": "Category 1",
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


def test_get_list_questions():
    data = [
        {
            "name": "Sanitation",
            "categories": [
                {
                    "name": "Basic",
                    "and": [{"question": 1, "options": ["Yes", "No"]}],
                    "or": [{"question": 2, "options": ["Clean", "Dirty"]}],
                }
            ],
        }
    ]

    lq = get_list_questions(data=data)
    assert lq == [
        {"question": 2, "options": ["Clean", "Dirty"]},
        {"question": 1, "options": ["Yes", "No"]},
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


def test_get_total_criteria_per_category():
    category = {
        "and": [
            {"question": 1, "options": ["Yes", "No"]},
            {"question": 2, "options": ["Yes", "No"]},
        ],
        "or": [{"question": 2, "options": ["Clean", "Dirty"]}],
    }

    total = get_total_criteria_per_category(category=category)
    assert total == 3
