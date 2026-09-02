"""Database utilities."""
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def get_engine():
    database_url = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/fakenews"
    )
    return create_engine(database_url, pool_size=10, max_overflow=20)


def get_session_factory():
    return sessionmaker(autocommit=False, autoflush=False, bind=get_engine())


@contextmanager
def get_db() -> Generator:
    SessionLocal = get_session_factory()
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def run_migrations() -> None:
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Migrations would run here via Alembic")


def seed_database() -> None:
    print("Seeding database with initial data...")
