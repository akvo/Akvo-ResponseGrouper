import json
import sys
import re

if len(sys.argv) < 2:
    print("You should provide json config file")
    exit(1)

f = open(sys.argv[1])
categories = json.load(f)
for c in categories:
    category_name = c.get("name")
    mview = f"SELECT data, '{category_name}' as name, category\n"
    mview += "FROM (\n"
    for union, category in enumerate(c.get("category")):
        name = category.get("name")
        group = re.sub('[^A-Za-z0-9]+', '_', name).lower()
        valid = 0
        if category.get("and"):
            valid += len(category.get("and"))
        if category.get("or"):
            valid += 1
        mview += f"  SELECT data, COUNT({group}), {valid} as valid,"
        mview += f" '{name}' as category\n"
        mview += "  FROM (SELECT data, CASE\n"
        if category.get("or"):
            for or_category in category.get("or"):
                question_id = or_category.get("question")
                for iop, opt in enumerate(or_category.get("options")):
                    mview += f"    WHEN ('{opt}' = ANY(options))"
                    mview += f" AND (question = {question_id}) THEN True\n"
                    if iop < (len(or_category.get("options")) - 1):
                        mview += "    OR\n"
        if category.get("and"):
            for or_category in category.get("and"):
                question_id = or_category.get("question")
                for iop, opt in enumerate(or_category.get("options")):
                    mview += f"    WHEN ('{opt}' = ANY(options))"
                    mview += f" AND (question = {question_id}) THEN True\n"
                    if iop < (len(or_category.get("options")) - 1):
                        mview += "    AND\n"
        mview += f"    END AS {group}\n"
        mview += "    FROM\n"
        mview += "    answer\n"
        mview += "   ) aw\n"
        mview += "  WHERE"
        mview += f" {group} = True\n"
        mview += "  GROUP BY data\n"
        if union < len(c.get("category")) - 1:
            mview += "  UNION\n"
    mview += ") d WHERE d.count = d.valid"
    print(mview)

f.close()
