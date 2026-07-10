"""Compatibility entry point that exposes all SQLAlchemy models."""
from app.models.audit_log import AuditLog
from app.models.doctor import Doctor
from app.models.followup import Followup
from app.models.hospital import Hospital
from app.models.interaction import Interaction, InteractionSource, MeetingType, Priority
from app.models.notification import Notification
from app.models.product import Product
from app.models.user import User, UserRole

__all__ = [
    "AuditLog",
    "Doctor",
    "Followup",
    "Hospital",
    "Interaction",
    "InteractionSource",
    "MeetingType",
    "Notification",
    "Priority",
    "Product",
    "User",
    "UserRole",
]
