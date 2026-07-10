"""Dashboard summary and analytics routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.db.database import get_db
from app.models.user import User
from app.models.doctor import Doctor
from app.models.interaction import Interaction
from app.models.followup import Followup
from app.schemas.dashboard import DashboardResponse, DashboardStats
from app.core.deps import get_current_user

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)

    total_doctors = db.query(Doctor).count()
    todays_meetings = (
        db.query(Interaction).filter(func.date(Interaction.meeting_date) == today).count()
    )
    pending_followups = db.query(Followup).filter(Followup.is_completed.is_(False)).count()
    completed_meetings = (
        db.query(Interaction).filter(Interaction.meeting_date < datetime.utcnow()).count()
    )
    monthly_meetings = (
        db.query(Interaction).filter(func.date(Interaction.meeting_date) >= month_start).count()
    )

    recent = (
        db.query(Interaction).order_by(Interaction.created_at.desc()).limit(10).all()
    )
    recent_activity = [
        {
            "id": i.id,
            "doctor_id": i.doctor_id,
            "notes": i.notes,
            "created_at": i.created_at.isoformat() if i.created_at else None,
        }
        for i in recent
    ]

    upcoming = (
        db.query(Followup)
        .filter(Followup.is_completed.is_(False), Followup.due_date >= datetime.utcnow())
        .order_by(Followup.due_date.asc())
        .limit(10)
        .all()
    )
    upcoming_followups = [
        {"id": f.id, "interaction_id": f.interaction_id, "due_date": f.due_date.isoformat()}
        for f in upcoming
    ]

    monthly_chart = []
    for i in range(5, -1, -1):
        month_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1) if i else month_start
        label = month_date.strftime("%b") if i else today.strftime("%b")
        monthly_chart.append({"month": label, "meetings": monthly_meetings if i == 0 else 0})

    return DashboardResponse(
        stats=DashboardStats(
            total_doctors=total_doctors,
            todays_meetings=todays_meetings,
            pending_followups=pending_followups,
            completed_meetings=completed_meetings,
            monthly_meetings=monthly_meetings,
        ),
        recent_activity=recent_activity,
        upcoming_followups=upcoming_followups,
        monthly_chart=monthly_chart,
    )


@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    by_priority = (
        db.query(Interaction.priority, func.count(Interaction.id))
        .group_by(Interaction.priority)
        .all()
    )
    by_specialization = (
        db.query(Doctor.specialization, func.count(Doctor.id))
        .group_by(Doctor.specialization)
        .all()
    )
    return {
        "by_priority": [{"label": p or "unset", "value": c} for p, c in by_priority],
        "by_specialization": [{"label": s or "unset", "value": c} for s, c in by_specialization],
    }
