from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DoctorBase(BaseModel):
    name: str
    specialization: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    hospital_id: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    city: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    hospital_id: Optional[str] = None


class DoctorOut(DoctorBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
