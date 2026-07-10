"""Follow-up reminder model."""
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class Followup(Base):
    __tablename__ = "followups"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    interaction_id = Column(String, ForeignKey("interactions.id"), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    interaction = relationship("Interaction", back_populates="followups")
