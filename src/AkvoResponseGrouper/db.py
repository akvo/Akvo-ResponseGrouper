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


def validate_question_options(
    connection, question, form, options: list = None
):
    try:
        query = text(
            "SELECT COUNT(*) as count FROM question "
            + "where id = :question AND "
            + "form = :form"
        )
        if options:
            query = text(
                "SELECT option.name FROM option "
                "JOIN question ON option.question = question.id "
                + "where option.name IN :options AND "
                + "option.question = :question AND "
                + "question.form = :form"
            )

        res = connection.execute(
            query,
            options=tuple(options) if options else [],
            question=question,
            form=form,
        )
        return [d[0] for d in res.fetchall()]
    except Exception:
        return False
