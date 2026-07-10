"""PostgreSQL SQLAlchemy engine, session, and startup connectivity helpers."""
import time
import sys

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings


if settings.DATABASE_URL.startswith("sqlite"):
    raise RuntimeError("SQLite is not supported. Use PostgreSQL via Docker Compose.")

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def wait_for_postgres(max_retries: int = 30, delay_seconds: int = 2) -> None:
    """Retry until PostgreSQL accepts connections or raise a clear error."""
    for attempt in range(1, max_retries + 1):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8")
            print("✅ PostgreSQL Connected Successfully")
            return
        except OperationalError as exc:
            if attempt == max_retries:
                raise RuntimeError(
                    "PostgreSQL is unavailable. Start it with `docker compose up -d` "
                    "and confirm `docker ps` shows ai-crm-postgres as healthy."
                ) from exc
            print(
                f"PostgreSQL unavailable; retrying connection "
                f"({attempt}/{max_retries})..."
            )
            time.sleep(delay_seconds)


def get_db():
    """FastAPI dependency that yields a database session per-request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
