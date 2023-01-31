import unittest
import json
from collections import defaultdict


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


class TestExample(unittest.TestCase):
    def test_if_duplicate_is_available(self):

        with open("./tests/category.json") as f:
            data = f.read()
            data = json.loads(data)

        options = []
        for categories in data[0]["categories"]:
            duplicates_dict = defaultdict()
            total = 1 if "or" in categories else 0
            list_questions = []
            if "or" in categories:
                list_questions += categories["or"]
            else:
                categories["or"] = []
            if "and" in categories:
                list_questions += categories["and"]
                total += len(categories["and"])
            duplicates = []
            for category in list_questions:
                for category_check in data[0]["categories"]:
                    for types in ["and", "or"]:
                        if types in category_check:
                            for ck in category_check[types]:
                                if (
                                    category_check["name"]
                                    != categories["name"]
                                ):
                                    if ck["question"] == category["question"]:
                                        intersect = intersection(
                                            ck["options"], category["options"]
                                        )
                                        if len(intersect):
                                            duplicates.append(
                                                {
                                                    "question": ck["question"],
                                                    "name": category_check[
                                                        "name"
                                                    ],
                                                    "option": ck["options"],
                                                    "type": types,
                                                }
                                            )
            for duplicate in duplicates:
                for types in ["and", "or"]:
                    dp = len(
                        list(
                            filter(
                                lambda x: x["type"] == types
                                and x["name"] == duplicate["name"]
                                and x["question"] == duplicate["question"],
                                duplicates,
                            )
                        )
                    )
                    if dp:
                        if duplicate["name"] in duplicates_dict:
                            if types in duplicates_dict[duplicate["name"]]:
                                duplicates_dict[duplicate["name"]][types] += 1
                            else:
                                duplicates_dict[duplicate["name"]][types] = 1
                            duplicates_dict[duplicate["name"]]["total"] += 1
                        else:
                            duplicates_dict[duplicate["name"]] = {
                                "and": 1 if "and" == types else 0,
                                "or": 1 if "or" == types else 0,
                                "total": 1,
                            }
            categories.update(
                {
                    "list_questions": list_questions,
                    "total": total,
                    "duplicates": duplicates,
                    "total_duplicate": dict(duplicates_dict),
                }
            )
            options.append(categories)
        printed = {}
        for opt in options:
            if opt["name"] in printed:
                continue
            for td in opt["total_duplicate"]:
                if opt["total_duplicate"][td]["total"] >= opt["total"]:
                    if opt["total_duplicate"][td]["or"] == len(
                        opt["or"]
                    ) and opt["total_duplicate"][td]["and"] == len(opt["and"]):
                        duplicate = list(
                            filter(
                                lambda x: x["name"] == td, opt["duplicates"]
                            )
                        )
                        print(f"POTENTIAL DUPLICATE: {opt['name']} WITH {td}")
                        for d in duplicate:
                            print(
                                f"""
                            QUESTION: {d['question']}
                            OPTIONS: {d['option']}
                            """
                            )
                        printed.update({td: True})
        self.assertEqual(len(printed), 1)


if __name__ == "__main__":
    unittest.main()
