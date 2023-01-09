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

start_time = time.process_time()
Base.metadata.create_all(bind=engine)
session = SessionLocal()

for table in ["answer", "data"]:
    action = truncate(session=session, table=table)
    print(action)

forms = session.query(Form).all()
fake = Faker()

repeats = 10
if len(sys.argv) > 1:
    print("Seed 10 Datapoints")
    repeats = sys.argv[1]

for form in forms:
    for i in range(1, int(repeats)):
        data = Data(
                form=form.id,
                name=fake.name(),
                created=datetime.now())
        for qg in form.question_group:
            for q in qg.question:
                answer = Answer(
                        question=q.id,
                        data=data.id)
                if len(q.option):
                    ox = random.randint(0, len(q.option) - 1)
                    opt = q.option[ox]
                    answer.options = [opt.name]
                if q.type == QuestionType.number:
                    answer.value = random.randint(1, 5)
                if q.type == QuestionType.text:
                    answer.text = fake.name()
                data.answer.append(answer)
        session.add(data)
        session.commit()
        session.refresh(data)
    print(f"ADDED {repeats} datapoint to {form.name}")