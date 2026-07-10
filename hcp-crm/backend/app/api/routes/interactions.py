"""Interaction CRUD routes (structured-form logging + history)."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.models.interaction import Interaction
from app.models.user import User
from app.schemas.interaction import InteractionCreate, InteractionUpdate, InteractionOut
from app.core.deps import get_current_user

router = APIRouter(prefix="/api", tags=["interactions"])


@router.get("/interaction", response_model=dict)
def list_interactions(
    doctor_id: Optional[str] = None,
    priority: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Interaction)
    if doctor_id:
        q = q.filter(Interaction.doctor_id == doctor_id)
    if priority:
        q = q.filter(Interaction.priority == priority)
    q = q.order_by(Interaction.meeting_date.desc())

    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.post("/interaction", response_model=InteractionOut)
def create_interaction(
    payload: InteractionCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    interaction = Interaction(**payload.model_dump(), rep_id=user.id)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.put("/interaction/{interaction_id}", response_model=InteractionOut)
def update_interaction(
    interaction_id: str,
    payload: InteractionUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(interaction, field, value)
    db.commit()
    db.refresh(interaction)
    return interaction


@router.delete("/interaction/{interaction_id}")
def delete_interaction(
    interaction_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    db.delete(interaction)
    db.commit()
    return {"detail": "Interaction deleted"}
