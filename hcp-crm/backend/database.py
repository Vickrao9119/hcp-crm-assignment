"""Compatibility entry point for the application's PostgreSQL database setup."""
from app.db.database import Base, SessionLocal, engine, get_db, wait_for_postgres

__all__ = ["Base", "SessionLocal", "engine", "get_db", "wait_for_postgres"]
