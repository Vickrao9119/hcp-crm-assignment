"""Doctor (HCP) CRUD routes with search, filter, and pagination."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorOut
from app.core.deps import get_current_user
from app.api.utils import get_or_404, paginate, apply_updates

router = APIRouter(prefix="/api", tags=["doctors"])


@router.get("/doctors", response_model=dict)
def list_doctors(
    search: Optional[str] = None,
    city: Optional[str] = None,
    specialization: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Doctor)
    if search:
        q = q.filter(Doctor.name.ilike(f"%{search}%"))
    if city:
        q = q.filter(Doctor.city == city)
    if specialization:
        q = q.filter(Doctor.specialization == specialization)

    return paginate(q, page, page_size)


@router.get("/doctors/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_or_404(db, Doctor, doctor_id, "Doctor not found")


@router.post("/doctor", response_model=DoctorOut)
def create_doctor(payload: DoctorCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    doctor = Doctor(**payload.model_dump(), created_by=user.id)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.put("/doctor/{doctor_id}", response_model=DoctorOut)
def update_doctor(
    doctor_id: str, payload: DoctorUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    doctor = get_or_404(db, Doctor, doctor_id, "Doctor not found")
    apply_updates(doctor, payload)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.delete("/doctor/{doctor_id}")
def delete_doctor(doctor_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    doctor = get_or_404(db, Doctor, doctor_id, "Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor deleted"}
