import itertools
from ..db import get_option_by_questions


def check_options(rows, questions: list, info: bool = True):
    errors = 0
    ls = [{"question": row["qid"], "option": row["name"]} for row in rows]
    for key, group in itertools.groupby(ls, key=lambda x: x["question"]):
        options = [o["option"] for o in list(group) if o["option"] is not None]
        fq = list(filter(lambda x: x["id"] == key, questions))
        if len(fq) and len(options):
            cg_items = set(fq[0]["options"])
            db_items = set(options)
            isec = set.intersection(cg_items, db_items)
            diff = list(cg_items - isec)
            if len(diff):
                errors += 1
                if info:
                    qid = fq[0]["id"]
                    print(
                        f"QUESTION ID: {qid} | options not found:"
                        f" {','.join(diff)}"
                    )
    return errors == 0


def check_questions(connection, questions: list, info: bool = True) -> bool:
    errors = 0
    ids = [q["id"] for q in questions]
    rq = get_option_by_questions(connection=connection, questions=ids)
    if rq:
        rows = set([row["qid"] for row in rq])
        diff = list(set(ids) - rows)
        if len(diff):
            errors += 1
            if info:
                qd = ", ".join([str(q) for q in diff])
                print(f"QUESTION ID NOT FOUND: {qd}")
        option_exists = check_options(rows=rq, questions=questions)
        if not option_exists:
            errors += 1
    return errors == 0
