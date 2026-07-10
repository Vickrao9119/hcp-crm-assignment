"""Compatibility entry point for database sessions."""
from app.db.database import SessionLocal, get_db

__all__ = ["SessionLocal", "get_db"]
