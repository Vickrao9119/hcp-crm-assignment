"""Shared CRUD helpers for simple SQLAlchemy model operations."""
from typing import Any, Type

from sqlalchemy.orm import Session


def get(db: Session, model: Type[Any], object_id: str) -> Any | None:
    return db.query(model).filter(model.id == object_id).first()


def create(db: Session, model: Type[Any], data: dict[str, Any]) -> Any:
    instance = model(**data)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update(db: Session, instance: Any, data: dict[str, Any]) -> Any:
    for field, value in data.items():
        setattr(instance, field, value)
    db.commit()
    db.refresh(instance)
    return instance


def delete(db: Session, instance: Any) -> None:
    db.delete(instance)
    db.commit()
