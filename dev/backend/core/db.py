from os import environ
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


def get_db_url():
    TESTING = environ.get("TESTING")
    DATABASE_URL = environ["DATABASE_URL"]
    DB_URL = f"{DATABASE_URL}_test" if TESTING else DATABASE_URL
    return DB_URL


engine = create_engine(get_db_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def truncate(session: Session, table: str):
    session.execute(f"TRUNCATE TABLE {table} CASCADE;")
    session.execute(f"ALTER SEQUENCE {table}_id_seq RESTART WITH 1;")
    session.execute(f"UPDATE {table} SET id=nextval('{table}_id_seq');")
    session.commit()
    session.flush()
    return f"{table} Truncated"

