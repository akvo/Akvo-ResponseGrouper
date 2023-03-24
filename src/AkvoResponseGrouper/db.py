from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy import inspect


def get_db_url():
    TESTING = environ.get("TESTING")
    DATABASE_URL = environ["DATABASE_URL"]
    DB_URL = f"{DATABASE_URL}_test" if TESTING else DATABASE_URL
    return DB_URL


engine = create_engine(get_db_url(), pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def view_exist():
    try:
        return inspect(engine).has_table("ar_category")
    except Exception:
        # to support legacy version 1.3
        return engine.has_table(table_name="ar_category")


def drop_view(connection):
    return connection.execute(text("DROP MATERIALIZED VIEW ar_category"))


def get_option_by_questions(connection, questions: list):
    try:
        query = text(
            "select option.*, question.id as qid, question.form as form"
            " from option "
            + "right join question on option.question = question.id "
            + "where question.id in :questions"
        )
        return connection.execute(
            query,
            questions=tuple(questions),
        ).fetchall()
    except Exception:
        return None
