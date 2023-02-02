import unittest
from AkvoResponseGrouper.cli.checker import check_config, get_options
from AkvoResponseGrouper.utils import generate_data_as_json_file


class TestCategoryChecker(unittest.TestCase):
    def test_if_category_is_typo(self):
        with self.assertRaises(SystemExit) as cm:
            data = {"name": "Water", "categoryies": []}
            get_options(data=data)
        self.assertEqual(cm.exception.code, 0)

    def test_name_is_not_present(self):
        data = [
            {
                "form": 2,
                "categories": [],
            }
        ]
        fc = generate_data_as_json_file(data=data)
        checker = check_config(file_config=fc, info=False)
        self.assertFalse(checker)

    def test_form_is_not_present(self):
        data = [
            {
                "name": "Water",
                "categories": [],
            }
        ]
        fc = generate_data_as_json_file(data=data)
        checker = check_config(file_config=fc, info=False)
        self.assertFalse(checker)

    def test_5C_duplicate_with_5CD(self):
        data = [
            {
                "name": "Water",
                "form": 1,
                "categories": [
                    {
                        "name": "Category-1A",
                        "and": [
                            {"question": 1, "options": ["A"]},
                        ],
                    },
                ],
            },
            {
                "name": "Sanitation",
                "form": 1,
                "categories": [
                    {
                        "name": "Category-5C",
                        "and": [
                            {"question": 5, "options": ["C"]},
                        ],
                    },
                    {
                        "name": "Category-5CD",
                        "and": [
                            {"question": 5, "options": ["C", "D"]},
                        ],
                    },
                ],
            },
        ]
        fc = generate_data_as_json_file(data=data)
        checker = check_config(file_config=fc, info=False)
        self.assertEqual(checker, 1)

    def test_1A_duplicate_with_1AB_and_1A_with_1AB2CD(self):
        data = [
            {
                "name": "Water",
                "form": 1,
                "categories": [
                    {
                        "name": "Category-1A",
                        "and": [
                            {"question": 1, "options": ["A"]},
                        ],
                    },
                    {
                        "name": "Category-1AB",
                        "and": [{"question": 1, "options": ["A", "B"]}],
                    },
                    {
                        "name": "Category-1AB2CD",
                        "and": [
                            {"question": 1, "options": ["A", "B"]},
                            {"question": 2, "options": ["C", "D"]},
                        ],
                    },
                ],
            }
        ]
        fc = generate_data_as_json_file(data=data)
        checker = check_config(file_config=fc, info=False)
        self.assertEqual(checker, 2)

    def test_checker_config_is_passed(self):
        data = [
            {
                "name": "Water",
                "form": 1,
                "categories": [
                    {
                        "name": "Category-1A3FG",
                        "and": [
                            {"question": 1, "options": ["A"]},
                            {"question": 3, "options": ["F", "G"]},
                        ],
                    },
                    {
                        "name": "Category-1AB",
                        "and": [
                            {"question": 1, "options": ["C"]},
                            {"question": 3, "options": ["A"]},
                        ],
                    },
                    {
                        "name": "Category-1AB2CD",
                        "and": [
                            {"question": 1, "options": ["A", "B"]},
                            {"question": 2, "options": ["C", "D"]},
                        ],
                    },
                ],
            }
        ]
        fc = generate_data_as_json_file(data=data)
        checker = check_config(file_config=fc, info=False)
        self.assertFalse(checker)


if __name__ == "__main__":
    unittest.main()
