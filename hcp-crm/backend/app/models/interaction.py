"""Interaction (HCP visit / meeting log) model."""
import enum
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class MeetingType(str, enum.Enum):
    IN_PERSON = "in_person"
    VIRTUAL = "virtual"
    PHONE = "phone"
    CONFERENCE = "conference"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InteractionSource(str, enum.Enum):
    FORM = "form"
    AI_CHAT = "ai_chat"


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = Column(String, ForeignKey("doctors.id"), nullable=False)
    rep_id = Column(String, ForeignKey("users.id"), nullable=False)

    meeting_date = Column(DateTime(timezone=True), nullable=False)
    meeting_type = Column(Enum(MeetingType), default=MeetingType.IN_PERSON)
    products_discussed = Column(String, nullable=True)  # comma-separated product names
    notes = Column(Text, nullable=True)
    samples_given = Column(Boolean, default=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM)
    follow_up_date = Column(DateTime(timezone=True), nullable=True)
    attachment_url = Column(String, nullable=True)

    ai_summary = Column(Text, nullable=True)
    ai_action_items = Column(Text, nullable=True)
    source = Column(Enum(InteractionSource), default=InteractionSource.FORM)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    doctor = relationship("Doctor", back_populates="interactions")
    followups = relationship("Followup", back_populates="interaction", cascade="all, delete-orphan")
