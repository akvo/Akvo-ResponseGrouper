from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_url():
    TESTING = environ.get("TESTING")
    DATABASE_URL = environ["DATABASE_URL"]
    DATABASE_URL = DATABASE_URL.replace("-", "_")
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
