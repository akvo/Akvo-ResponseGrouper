import unittest
from AkvoResponseGrouper.cli.checker import check_config
from AkvoResponseGrouper.utils import generate_data_as_json_file


class TestCategoryChecker(unittest.TestCase):
    def test_if_duplicate_is_available(self):
        fake_data = [
            {
                "name": "Water",
                "form": "556240162",
                "categories": [
                    {
                        "name": "Unimproved D",
                        "and": [
                            {
                                "question": 573340127,
                                "options": ["Bottled water"],
                            },
                            {
                                "question": 573340129,
                                "options": ["Bottled water"],
                            },
                        ],
                    },
                    {
                        "name": "Unimproved C",
                        "or": [
                            {
                                "question": 573340127,
                                "options": ["Bottled water"],
                            },
                            {"question": 999, "options": ["Bottled water"]},
                        ],
                        "and": [
                            {
                                "question": 573340129,
                                "options": ["Bottled water"],
                            }
                        ],
                    },
                    {
                        "name": "Surface Water",
                        "and": [
                            {
                                "question": 573340127,
                                "options": ["Surface water"],
                            }
                        ],
                    },
                    {
                        "name": "Unimproved",
                        "and": [
                            {
                                "question": 573340127,
                                "options": [
                                    "Bottled water",
                                    "Unprotected spring",
                                    "Unprotected dug well",
                                ],
                            },
                            {
                                "question": 573340129,
                                "options": ["Bottled water"],
                            },
                        ],
                    },
                    {
                        "name": "Limited",
                        "and": [
                            {
                                "question": 573340127,
                                "options": [
                                    "Protected dug well",
                                    "Public tap/standpipe",
                                    (
                                        "Piped water into dwelling (household"
                                        " connection)"
                                    ),
                                    "Piped to neighbour",
                                    "Piped water to yard/plot",
                                    (
                                        "Shared Deep tube well / shallow tube"
                                        " well"
                                    ),
                                    "Shallow tubewell/borehole",
                                    "Protected spring",
                                    "Deep tubewell/borehole",
                                ],
                            },
                            {
                                "question": 573340128,
                                "options": ["More than 30 minutes"],
                            },
                        ],
                    },
                    {
                        "name": "Basic",
                        "and": [
                            {
                                "question": 573340127,
                                "options": [
                                    "Protected dug well",
                                    "Public tap/standpipe",
                                    (
                                        "Piped water into dwelling (household"
                                        " connection)"
                                    ),
                                    "Piped to neighbour",
                                    "Piped water to yard/plot",
                                    (
                                        "Shared Deep tube well / shallow tube"
                                        " well"
                                    ),
                                    "Shallow tubewell/borehole",
                                    "Protected spring",
                                    "Deep tubewell/borehole",
                                ],
                            },
                            {
                                "question": 573340128,
                                "options": [
                                    "Less than 30 minutes",
                                    "Don''t know",
                                ],
                            },
                            {
                                "question": 573340129,
                                "options": [
                                    "Yes, at least once",
                                    "Don''t know",
                                ],
                            },
                        ],
                    },
                    {
                        "name": "Safely Managed",
                        "and": [
                            {
                                "question": 573340127,
                                "options": [
                                    "Protected dug well",
                                    "Public tap/standpipe",
                                    (
                                        "Piped water into dwelling (household"
                                        " connection)"
                                    ),
                                    "Piped to neighbour",
                                    "Piped water to yard/plot",
                                    (
                                        "Shared Deep tube well / shallow tube"
                                        " well"
                                    ),
                                    "Shallow tubewell/borehole",
                                    "Protected spring",
                                    "Deep tubewell/borehole",
                                ],
                            },
                            {
                                "question": 573340128,
                                "options": [
                                    "Less than 30 minutes",
                                    "Don''t know",
                                ],
                            },
                            {
                                "question": 573340129,
                                "options": ["No, always sufficient"],
                            },
                            {
                                "question": 573340125,
                                "options": [
                                    "Free from feacal and prioirty chemical"
                                    " contamination"
                                ],
                            },
                        ],
                    },
                ],
            }
        ]
        file = generate_data_as_json_file(data=fake_data)
        checker = check_config(file_config=file)
        self.assertTrue(checker)


if __name__ == "__main__":
    unittest.main()
