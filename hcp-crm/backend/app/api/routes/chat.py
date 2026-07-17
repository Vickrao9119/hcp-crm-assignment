"""AI Chat route — runs the LangGraph agent and optionally persists an interaction."""
import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.models.user import User
from app.models.doctor import Doctor
from app.models.interaction import Interaction, InteractionSource
from app.schemas.chat import ChatMessageIn, ChatMessageOut
from app.core.deps import get_current_user
from app.agent.graph import run_agent

router = APIRouter(prefix="/api", tags=["chat"])

logger = logging.getLogger(__name__)


@router.post("/chat", response_model=ChatMessageOut)
def chat(payload: ChatMessageIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    session_id = payload.session_id or str(uuid.uuid4())
    result = run_agent(payload.message)

    interaction_saved = False
    interaction_id = None

    if result.get("intent") == "log_interaction":
        entities = result.get("entities", {})
        try:
            doctor = None
            if entities.get("doctor"):
                doctor = db.query(Doctor).filter(Doctor.name.ilike(f"%{entities['doctor'].replace('Dr. ', '')}%")).first()
                if not doctor:
                    doctor = Doctor(name=entities["doctor"], created_by=user.id)
                    db.add(doctor)
                    db.commit()
                    db.refresh(doctor)

            if doctor:
                interaction = Interaction(
                    doctor_id=doctor.id,
                    rep_id=user.id,
                    meeting_date=datetime.utcnow(),
                    products_discussed=", ".join(entities.get("products", [])),
                    notes=payload.message,
                    samples_given=entities.get("samples_requested", False),
                    priority=entities.get("priority", "medium"),
                    ai_summary=result.get("tool_result", {}).get("summary"),
                    source=InteractionSource.AI_CHAT,
                )
                db.add(interaction)
                db.commit()
                db.refresh(interaction)
                interaction_saved = True
                interaction_id = interaction.id
        except SQLAlchemyError:
            # Roll back so the session isn't left in a broken state, and surface
            # the failure instead of returning a misleading success response.
            db.rollback()
            logger.exception("Failed to persist AI-chat interaction")
            raise HTTPException(
                status_code=500, detail="Failed to save interaction from chat."
            )

    return ChatMessageOut(
        reply=result.get("reply", ""),
        session_id=session_id,
        extracted_entities=result.get("entities"),
        interaction_saved=interaction_saved,
        interaction_id=interaction_id,
    )
