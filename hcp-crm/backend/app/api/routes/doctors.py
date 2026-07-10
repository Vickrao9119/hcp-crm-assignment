"""Doctor (HCP) CRUD routes with search, filter, and pagination."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from app.db.database import get_db
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorOut
from app.core.deps import get_current_user

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

    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


@router.get("/doctors/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


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
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(doctor, field, value)
    db.commit()
    db.refresh(doctor)
    return doctor


@router.delete("/doctor/{doctor_id}")
def delete_doctor(doctor_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"detail": "Doctor deleted"}
