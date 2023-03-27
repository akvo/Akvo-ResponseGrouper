import os
from ..utils import (
    group_by_category_output,
    get_intersection,
    generate_data_as_json_file,
    get_valid_list,
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
                "else": {"name": "No Service"},
            },
            {
                "id": 567800083,
                "name": "Share with outside member?",
                "options": ["No"],
                "else": {"name": "Limited"},
            },
            {
                "id": 567800083,
                "name": "A",
                "options": ["Boys n Girls"],
                "else": {"name": "Limited"},
            },
        ],
    }
    category = False
    _category = get_valid_list(opt, c, category)
    assert _category == "Limited"
