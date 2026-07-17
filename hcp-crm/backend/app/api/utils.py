"""Shared helpers for API routes: 404 lookups, pagination, and partial updates.

These consolidate patterns that were previously duplicated across the doctor,
interaction, and notification routers.
"""
from typing import Type, TypeVar

from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Query, Session

ModelT = TypeVar("ModelT")


def get_or_404(db: Session, model: Type[ModelT], obj_id, detail: str) -> ModelT:
    """Fetch a row by primary-key ``id`` or raise a 404 with ``detail``."""
    obj = db.query(model).filter(model.id == obj_id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail=detail)
    return obj


def paginate(query: Query, page: int, page_size: int) -> dict:
    """Return a standard paginated envelope for a SQLAlchemy query."""
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def apply_updates(instance, payload: BaseModel) -> None:
    """Apply a partial-update payload onto a model instance in place."""
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(instance, field, value)
