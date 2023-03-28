import itertools
from ..db import get_option_by_questions


def check_options(rows, questions: list) -> list:
    errors = []
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
                errors.append(
                    {
                        "error": "options",
                        "form": fq[0]["form"],
                        "question": fq[0]["id"],
                        "diff": diff,
                    }
                )
    return errors


def check_questions(connection, questions: list) -> list:
    errors = []
    for frm, qs in itertools.groupby(questions, key=lambda x: x["form"]):
        lqs = list(qs)
        ids = [q["id"] for q in lqs]
        res = get_option_by_questions(connection=connection, questions=ids)
        if res:
            dbqs = list(set([lt["qid"] for lt in list(res)]))
            diff = list(set(ids) - set(dbqs))
            if len(diff):
                errors.append({"error": "question", "diff": diff})
            errors += check_options(rows=res, questions=lqs)
    return errors


def get_error_messages(
    value: int, form: int = None, question: int = None
) -> str:
    msg = f"QUESTION: {value} not found"
    if form and question:
        msg = (
            f"OPTION : {value} is not part of FORM: {form} | QUESTION:"
            f" {question}"
        )
    if form and question is None:
        msg = f"QUESTION: {value} is not part of FORM: {form}"
    return msg


def print_error_questions(errors: list):
    for error in errors:
        for diff in error["diff"]:
            msg = get_error_messages(
                value=diff,
                form=error.get("form"),
                question=error.get("question"),
            )
            print(msg, "\n===================")
