"""Compatibility entry point that exposes Pydantic schemas."""
from app.schemas.chat import ChatMessageIn, ChatMessageOut
from app.schemas.dashboard import DashboardResponse, DashboardStats
from app.schemas.doctor import DoctorCreate, DoctorOut, DoctorUpdate
from app.schemas.interaction import InteractionCreate, InteractionOut, InteractionUpdate
from app.schemas.user import Token, UserCreate, UserLogin, UserOut

__all__ = [
    "ChatMessageIn",
    "ChatMessageOut",
    "DashboardResponse",
    "DashboardStats",
    "DoctorCreate",
    "DoctorOut",
    "DoctorUpdate",
    "InteractionCreate",
    "InteractionOut",
    "InteractionUpdate",
    "Token",
    "UserCreate",
    "UserLogin",
    "UserOut",
]
