import json


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


def check_config(file_config: str, info: bool = True):
    with open(file_config) as f:
        data = f.read()
        data = json.loads(data)
    errors = []
    questions = []
    for config in data:
        qs = []
        for c in config["categories"]:
            cname = config.get("name")
            find_errors_in_questions(
                config=c, errors=errors, name=cname
            )
            qs = get_all_questions(config=c, qs=qs)
            questions.append(qs)
    if info:
        print_errors_no_category(errors=errors)
    return errors, questions
