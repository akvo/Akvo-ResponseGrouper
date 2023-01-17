from ..utils import group_by_category_output

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
