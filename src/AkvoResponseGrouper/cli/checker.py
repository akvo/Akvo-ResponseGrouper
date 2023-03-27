import json
from ..utils import flatten_list


def find_errors_in_questions(
    config: dict,
    errors: list,
    name: str,
    form: int,
    question=None,
    other=False,
) -> None:
    errors = []
    if "name" not in config:
        errors.append(
            {
                "name": name,
                "question": question,
                "form": form,
                "error": "name",
                "other": other,
            }
        )
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
                ek = False if "ignore" in q["else"] else True
                errors.append(
                    {
                        "name": name,
                        "question": q.get("id"),
                        "form": form,
                        "error": "name",
                        "other_key": other,
                        "else_key": ek,
                    }
                )


def find_errors_in_config(config: dict, name: str) -> list:
    errors = []
    if "form" not in config:
        errors.append({"name": name, "error": "form"})
    if "categories" not in config:
        errors.append({"name": name, "error": "categories"})
    return errors


def get_all_questions(config: dict, form: str, qs: list) -> list:
    for q in config.get("questions"):
        qs.append(
            {
                "category": config.get("name"),
                "form": form,
                "id": q.get("id"),
                "options": q.get("options"),
            }
        )
        if q.get("other"):
            for o in q.get("other"):
                get_all_questions(
                    config=o,
                    form=form,
                    qs=qs,
                )
    return qs


def get_error_messages(errors: list) -> list:
    messages = []
    for error in errors:
        prefix = f"NAME: {error['name']} | " if "name" in error else ""
        if error.get("form"):
            msg = f"{prefix}FORM: {error['form']} | "
            if "question" in error:
                msg += f"QUESTION: {error['question']} | "
            key_name = (
                "`other`"
                if error.get("other_key")
                else "`else`"
                if error.get("else_key")
                else "`categories`"
            )
            msg += f"CATEGORY NAME is required in {key_name}"
        if error["error"] == "form":
            msg = f"{prefix}FORM is required"
        if error["error"] == "categories":
            msg = f"{prefix}`categories` is typo or not present"
        messages.append(msg)
    return messages


def get_potential_duplicates(items: list) -> list:
    duplicates = []
    counts = {}
    for item in items:
        form = item["form"]
        for question in item["questions"]:
            key = (form, question["id"])
            counts[key] = counts.get(key, 0) + 1
    unique = set(counts.values())
    qs = flatten_list(ld=[i["questions"] for i in items])
    if len(unique) > 1:
        mv = max(unique)
        cl = list(counts.values())
        for ix, obj in enumerate(list(counts)):
            f, q = obj
            if cl[ix] == mv:
                categories = set(
                    [
                        lt["category"]
                        for lt in list(
                            filter(
                                lambda x: x["form"] == f and x["id"] == q,
                                qs,
                            )
                        )
                    ]
                )
                if len(categories) == 2:
                    a, b = categories
                    msg = (
                        f"POTENTIAL DUPLICATE: {a} with {b} by\n"
                        f"FORM ID: {f} | QUESTION: {q}"
                    )
                    duplicates.append(msg)
    return duplicates


def check_config(file_config: str, info: bool = True):
    with open(file_config) as f:
        data = f.read()
        data = json.loads(data)
    errors = []
    items = []
    for config in data:
        qs = []
        cname = config.get("name")
        errors += find_errors_in_config(config=config, name=cname)

        if "form" in config and "categories" in config:
            for c in config["categories"]:
                find_errors_in_questions(
                    config=c, errors=errors, name=cname, form=config["form"]
                )
                qs = get_all_questions(config=c, form=config["form"], qs=qs)
                items.append(
                    {
                        "form": config["form"],
                        "questions": qs,
                    }
                )
    duplicates = get_potential_duplicates(items=items)
    questions = [i["questions"] for i in items]
    errors = get_error_messages(errors=errors)
    if info:
        for error in errors:
            print(error, "\n=============================")
    return errors, questions, duplicates
