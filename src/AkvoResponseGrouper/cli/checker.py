import json
import itertools
from ..db import get_option_by_questions


def find_errors_in_questions(
    config: dict, errors: list, name: str, question=None, other=False
) -> list:
    if "name" not in config:
        errors.append({"name": name, "q": question, "o": other})
    for q in config.get("questions"):
        for o in q.get("other") if "other" in q else []:
            find_errors_in_questions(
                config=o,
                errors=errors,
                name=name,
                question=q.get("id"),
                other=True,
            )
        if "else" in q:
            if not len(
                set.intersection(
                    set(q["else"].keys()), set(["name", "ignore"])
                )
            ):
                else_key = False if "ignore" in q["else"] else True
                errors.append({"name": name, "q": q.get("id"), "e": else_key})


def get_all_questions(config: dict, qs: list) -> list:
    for q in config.get("questions"):
        qs.append({"id": q.get("id"), "options": q.get("options")})
        if q.get("other"):
            for o in q.get("other"):
                get_all_questions(
                    config=o,
                    qs=qs,
                )
    return qs


def print_errors_no_category(errors: list):
    for error in errors:
        en = error["name"]
        eq = error["q"]
        eo = error.get("o")
        ek = error.get("e")
        print(
            f"{en} |",
            f"QUESTION ID: {eq}|" if eq else "",
            "NAME is required",
            "in `other` key."
            if eo
            else "in `else` key"
            if ek
            else "before `questions` key",
        )


def print_dup_questions(form_questions: dict, same_questions: set):
    if len(same_questions) and len(form_questions) > 1:
        dq = ", ".join(str(q) for q in same_questions)
        print(f"POTENTIAL DUPLICATE: have more than one question id: {dq}")


def check_config(file_config: str, info: bool = True):
    with open(file_config) as f:
        data = f.read()
        data = json.loads(data)
    form_questions = {}
    errors = []
    questions = []
    for config in data:
        qs = []
        for c in config["categories"]:
            find_errors_in_questions(
                config=c, errors=errors, name=config["name"]
            )
            qs = get_all_questions(config=c, qs=qs)
            questions.append(qs)
        form = config["form"]
        ql = [q["id"] for q in qs]
        if form not in form_questions:
            form_questions[form] = set(ql)
        else:
            form_questions[form].update(ql)
    same_questions = set.intersection(*form_questions.values())
    if info:
        print_errors_no_category(errors=errors)
        print_dup_questions(
            form_questions=form_questions, same_questions=same_questions
        )

    if len(same_questions) and len(form_questions) > 1:
        errors.append(same_questions)
    return errors, questions


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
