from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ChatMessageIn(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatMessageOut(BaseModel):
    reply: str
    session_id: str
    extracted_entities: Optional[Dict[str, Any]] = None
    interaction_saved: bool = False
    interaction_id: Optional[str] = None
