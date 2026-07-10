from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InteractionBase(BaseModel):
    doctor_id: str
    meeting_date: datetime
    meeting_type: Optional[str] = "in_person"
    products_discussed: Optional[str] = None
    notes: Optional[str] = None
    samples_given: Optional[bool] = False
    priority: Optional[str] = "medium"
    follow_up_date: Optional[datetime] = None
    attachment_url: Optional[str] = None


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    meeting_date: Optional[datetime] = None
    meeting_type: Optional[str] = None
    products_discussed: Optional[str] = None
    notes: Optional[str] = None
    samples_given: Optional[bool] = None
    priority: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    attachment_url: Optional[str] = None


class InteractionOut(InteractionBase):
    id: str
    rep_id: str
    ai_summary: Optional[str] = None
    ai_action_items: Optional[str] = None
    source: str
    created_at: datetime

    class Config:
        from_attributes = True
