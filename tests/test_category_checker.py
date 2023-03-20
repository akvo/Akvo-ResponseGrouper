import unittest
from AkvoResponseGrouper.cli.checker import check_config
from AkvoResponseGrouper.utils import generate_data_as_json_file


class TestCategoryChecker(unittest.TestCase):
    def test_category_name_is_not_present_in_specified_keys(self):
        # a list of key that required to have `name` field
        # > namely: category, other, and else
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
        errors, questions = check_config(file_config=fc, info=False)
        self.assertEqual(len(errors), 3)

    def test_duplicate_question_11CD_with_11FG(self):
        # Different form ids have the same question id.
        data = [
            {
                "form": 1,
                "categories": [
                    {
                        "name": "Category-11CD",
                        "questions": [{"id": 11, "options": ["C", "D"]}],
                    }
                ],
            },
            {
                "form": 4,
                "categories": [
                    {
                        "name": "Category-11FG",
                        "questions": [{"id": 11, "options": ["F", "G"]}],
                    }
                ],
            },
        ]
        fc = generate_data_as_json_file(data=data)
        errors, questions = check_config(file_config=fc, info=False)
        self.assertEqual(len(errors), 1)


if __name__ == "__main__":
    unittest.main()
