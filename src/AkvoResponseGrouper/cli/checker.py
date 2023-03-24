import json


def find_errors_in_questions(
    config: dict,
    errors: list,
    name: str,
    form: int,
    question=None,
    other=False,
) -> list:
    if "name" not in config:
        err1 = (
            f"{name}FORM: {form} | QUESTION: {question} | "
            "CATEGORY NAME is required"
            if question
            else f"{name}FORM: {form} | CATEGORY NAME is required"
        )
        err1 += " in `other`" if other else " in `categories`"
        errors.append(err1)
    for q in config.get("questions"):
        for o in q.get("other") if "other" in q else []:
            find_errors_in_questions(
                config=o,
                errors=errors,
                name=name,
                form=form,
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
                qid = q.get("id")
                err2 = (
                    f"{name}FORM: {form} | QUESTION: {qid} | CATEGORY NAME is"
                )
                err2 += (
                    " required in `else`"
                    if else_key
                    else " required in `categories`"
                )
                errors.append(err2)


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


def print_errors_no_category(errors: list, info: bool = True):
    if info:
        for error in errors:
            print(error)
            print("=============================")


def check_config(file_config: str, info: bool = True):
    with open(file_config) as f:
        data = f.read()
        data = json.loads(data)
    errors = []
    questions = []
    for config in data:
        qs = []
        cname = config.get("name")
        pname = f"NAME: {cname} | " if cname else ""
        if "form" not in config:
            errors.append(f"{pname}FORM is required")
        if "categories" not in config:
            errors.append(f"{pname}`categories` is typo or not present")
        if "form" in config and "categories" in config:
            for c in config["categories"]:
                find_errors_in_questions(
                    config=c, errors=errors, name=pname, form=config["form"]
                )
                qs = get_all_questions(config=c, qs=qs)
                questions.append(qs)
    print_errors_no_category(errors=errors, info=info)
    return errors, questions
