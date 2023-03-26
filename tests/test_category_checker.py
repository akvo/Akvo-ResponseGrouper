import unittest
from AkvoResponseGrouper.cli.checker import check_config
from AkvoResponseGrouper.utils import generate_data_as_json_file


class TestCategoryChecker(unittest.TestCase):
    def test_if_category_is_typo(self):
        data = [
            {
                "name": "Water",
                "form": 1,
                "categoriyes": [],
            }
        ]
        fc = generate_data_as_json_file(data=data)
        errors, q, d = check_config(file_config=fc, info=False)
        if len(errors):
            self.assertEqual(
                errors[0], "NAME: Water | `categories` is typo or not present"
            )

    def test_name_is_not_present(self):
        data = [
            {
                "form": 2,
                "categories": [
                    {
                        "questions": [
                            {
                                "id": 1,
                                "options": ["A", "B"],
                                "other": [{"questions": []}],
                                "else": {},
                            }
                        ],
                    }
                ],
            }
        ]
        fc = generate_data_as_json_file(data=data)
        errors, q, d = check_config(file_config=fc, info=False)
        if len(errors):
            self.assertEqual(
                errors[0],
                "FORM: 2 | CATEGORY NAME is required in `categories`",
            )
            self.assertEqual(
                errors[1],
                "FORM: 2 | QUESTION: 1 | CATEGORY NAME is required in `other`",
            )
            self.assertEqual(
                errors[2],
                "FORM: 2 | QUESTION: 1 | CATEGORY NAME is required in `else`",
            )

    def test_form_is_not_present(self):
        data = [
            {
                "name": "Water",
                "categories": [],
            }
        ]
        fc = generate_data_as_json_file(data=data)
        errors, q, d = check_config(file_config=fc, info=False)
        self.assertEqual(len(errors), 1)
        if len(errors):
            self.assertEqual(errors[0], "NAME: Water | FORM is required")

    def test_5C_duplicate_with_1CD5CD(self):
        data = [
            {
                "name": "Water",
                "form": 1,
                "categories": [
                    {
                        "name": "Category-5C",
                        "questions": [{"id": 5, "options": ["C"]}],
                    }
                ],
            },
            {
                "name": "Water",
                "form": 1,
                "categories": [
                    {
                        "name": "Category-1AB",
                        "questions": [
                            {
                                "id": 1,
                                "options": ["A", "B"],
                                "other": [
                                    {
                                        "name": "Category-1CD5CD",
                                        "options": ["C", "D"],
                                        "questions": [
                                            {"id": 5, "options": ["C", "D"]}
                                        ],
                                    }
                                ],
                            }
                        ],
                    }
                ],
            },
        ]
        fc = generate_data_as_json_file(data=data)
        e, q, duplicates = check_config(file_config=fc, info=False)
        if len(duplicates):
            self.assertTrue(
                "Category-1CD5CD" in duplicates[0]
                and "Category-5C" in duplicates[0]
            )

    def test_checker_config_is_passed(self):
        data = [
            {
                "name": "Water",
                "form": 1,
                "categories": [
                    {
                        "name": "Category-1A3FG",
                        "questions": [
                            {"id": 1, "options": ["A"]},
                            {
                                "id": 3,
                                "options": ["F", "G"],
                                "other": [
                                    {
                                        "name": "Category-3BD",
                                        "options": ["B", "D"],
                                        "questions": [],
                                    }
                                ],
                                "else": {"name": "Category-3X"},
                            },
                        ],
                    }
                ],
            }
        ]
        fc = generate_data_as_json_file(data=data)
        errors, q, d = check_config(file_config=fc, info=False)
        self.assertCountEqual(errors, [])  # no errors


if __name__ == "__main__":
    unittest.main()
