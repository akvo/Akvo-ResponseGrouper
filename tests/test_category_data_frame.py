import unittest
from AkvoResponseGrouper.utils import (
    generate_data_as_json_file,
    transform_categories_to_df,
)


class TestCategoryDataFrame(unittest.TestCase):
    def test_df_to_get_limited_category(self):
        category = [
            {
                "name": "Water",
                "form": 1,
                "categories": [
                    {
                        "name": "Basic",
                        "questions": [
                            {
                                "id": 567800081,
                                "text": "Saperate Toilet",
                                "options": ["Yes"],
                                "else": {"name": "Limited"},
                            }
                        ],
                    }
                ],
            }
        ]
        fc = generate_data_as_json_file(data=category)
        categories = [
            {
                "id": 1,
                "data": 1,
                "form": 1,
                "name": "Water",
                "opt": {
                    "567800081": ["No"],
                },
            }
        ]
        records = transform_categories_to_df(
            categories=categories, file_path=fc
        ).to_dict("records")
        assert records == [
            {
                "id": 1,
                "data": 1,
                "form": 1,
                "name": "Water",
                "category": "Limited",
            }
        ]


if __name__ == "__main__":
    unittest.main()
