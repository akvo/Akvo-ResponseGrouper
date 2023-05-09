import itertools
from ..db import validate_question_options


def check_questions(connection, questions: list) -> list:
    errors = []
    for frm, qs in itertools.groupby(questions, key=lambda x: x["form"]):
        for qs in list(qs):
            check_from_db = validate_question_options(
                connection=connection,
                options=qs["options"],
                question=qs["id"],
                form=frm,
            )
            if check_from_db and qs["options"]:
                diff = set.difference(set(qs["options"]), set(check_from_db))
                if len(diff):
                    errors.append(
                        {
                            "error": "options",
                            "form": frm,
                            "question": qs["id"],
                            "diff": diff,
                        }
                    )
            if not check_from_db:
                errors.append(
                    {
                        "error": "question",
                        "form": frm,
                        "question": qs["id"],
                        "diff": [qs["id"]],
                    }
                )
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
