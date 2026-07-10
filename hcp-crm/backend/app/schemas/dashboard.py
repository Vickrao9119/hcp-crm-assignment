from pydantic import BaseModel
from typing import List, Dict, Any


class DashboardStats(BaseModel):
    total_doctors: int
    todays_meetings: int
    pending_followups: int
    completed_meetings: int
    monthly_meetings: int


class DashboardResponse(BaseModel):
    stats: DashboardStats
    recent_activity: List[Dict[str, Any]]
    upcoming_followups: List[Dict[str, Any]]
    monthly_chart: List[Dict[str, Any]]
