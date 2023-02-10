import json
import os
import time
from datetime import timedelta
from core.db import Base, SessionLocal, engine
from core.db import truncate
from models.form import Form
from models.question_group import QuestionGroup
from models.question import Question
from models.option import Option
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Base.metadata.create_all(bind=engine)


def seed(session: Session, file_path: str) -> None:
    start_time = time.process_time()
    for table in ["form", "question_group", "question",
                  "option", "data", "answer"]:
        action = truncate(session=session, table=table)
        print(action)

    with open(f"{file_path}") as json_file:
        json_form = json.load(json_file)

    form = Form(id=json_form["id"], name=json_form["name"])
    session.add(form)
    session.commit()
    session.refresh(form)

    for qgi, qg in enumerate(json_form["question_groups"]):
        question_group = QuestionGroup(
            name=qg["question_group"], order=qgi, form=form.id
        )
        session.add(question_group)
        session.commit()
        session.refresh(question_group)
        print(f"Question Group: {question_group.name}")
        for i, q in enumerate(qg["questions"]):
            question = Question(
                id=q["id"] if "id" in q else None,
                name=q["name"],
                order=q["order"],
                form=form.id,
                question_group=question_group.id,
                type=q["type"],
                dependency=q["dependency"] if "dependency" in q else None
            )
            if q.get("options"):
                for o in q["options"]:
                    option = Option(name=o["name"])
                    question.option.append(option)
            session.add(question)
            session.commit()
            session.refresh(question)
            print(f"{i}.{question.name}")
    print("------------------------------------------")

    elapsed_time = time.process_time() - start_time
    elapsed_time = str(timedelta(seconds=elapsed_time)).split(".")[0]
    print(f"\n-- DONE IN {elapsed_time}\n")
    return None


def main(session: Session, file_path: str) -> None:
    seed(session=session, file_path=file_path)


if __name__ == "__main__":
    session = SessionLocal()

    main(session=session, file_path="./sources/real-form.json")
