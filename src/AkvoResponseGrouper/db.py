from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


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


def get_existing_view(connection):
    return connection.execute(
        text(
            """
                SELECT count(relkind) from pg_class
                where relname = 'ar_category'
                and relkind = 'm'
                """
        )
    ).fetchone()


def drop_view(connection):
    return connection.execute(text("DROP MATERIALIZED VIEW ar_category"))
