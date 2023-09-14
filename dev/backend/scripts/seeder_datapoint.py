import sys
import time
import random
from datetime import datetime
from faker import Faker
from models.form import Form
from models.data import Data
from models.question import QuestionType
from models.answer import Answer
from core.db import Base, SessionLocal, engine, truncate
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from AkvoResponseGrouper.views import refresh_view

start_time = time.process_time()
Base.metadata.create_all(bind=engine)
session = SessionLocal()


def generate_answer(data, form, fake) -> None:
    answered_data = []
    for qg in form.question_group:
        repeats = random.randint(0, 3) if qg.repeatable else 1
        for repeat_index in range(repeats):
            for q in qg.question:
                answer = Answer(
                    question=q.id, data=data.id, repeat=repeat_index
                )
                if q.dependency:
                    valid = 0
                    for d in q.dependency:
                        answered = list(
                            filter(lambda x: x["id"] == d["id"], answered_data)
                        )
                        if len(answered):
                            if len(
                                set(answered[0]["options"]).intersection(
                                    d["options"]
                                )
                            ):
                                valid += 1
                    if valid != len(q.dependency):
                        continue
                if len(q.option):
                    ox = random.randint(0, len(q.option) - 1)
                    opt = q.option[ox]
                    answer.options = [opt.name]
                if q.type == QuestionType.number:
                    # 0 For No Service Test
                    answer.value = random.randint(0 if q.id == 999 else 1, 5)
                if q.type == QuestionType.text:
                    answer.text = fake.name()
                aw = answer.options or answer.value or answer.text
                if aw:
                    answered_data.append({"id": q.id, "options": aw})
                    data.answer.append(answer)


def seed(session=Session, repeats=int) -> None:
    for table in ["answer", "data"]:
        action = truncate(session=session, table=table)
        print(action)

    forms = session.query(Form).all()
    fake = Faker()

    for form in forms:
        for i in range(1, int(repeats)):
            data = Data(form=form.id, name=fake.name(), created=datetime.now())
            generate_answer(data, form, fake)
            session.add(data)
            session.commit()
            session.refresh(data)
        print(f"ADDED {repeats} datapoint to {form.name}")

    if inspect(engine).has_table("ar_category"):
        refresh_view(session)


def main(session=Session, repeats=int):
    seed(session=session, repeats=repeats)


if __name__ == "__main__":
    repeats = 10
    if len(sys.argv) > 1:
        repeats = sys.argv[1]
        print(f"Seed {repeats} Datapoints")
    main(session=session, repeats=repeats)
