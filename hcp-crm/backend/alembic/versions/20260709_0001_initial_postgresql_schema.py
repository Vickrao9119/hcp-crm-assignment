"""Initial PostgreSQL schema.

Revision ID: 20260709_0001
Revises:
Create Date: 2026-07-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260709_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


meeting_type = sa.Enum(
    "IN_PERSON",
    "VIRTUAL",
    "PHONE",
    "CONFERENCE",
    name="meetingtype",
)
priority = sa.Enum("LOW", "MEDIUM", "HIGH", name="priority")
interaction_source = sa.Enum("FORM", "AI_CHAT", name="interactionsource")
user_role = sa.Enum("ADMIN", "MANAGER", "MEDICAL_REP", name="userrole")


def upgrade() -> None:
    bind = op.get_bind()
    meeting_type.create(bind, checkfirst=True)
    priority.create(bind, checkfirst=True)
    interaction_source.create(bind, checkfirst=True)
    user_role.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)

    op.create_table(
        "hospitals",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_hospitals_name"), "hospitals", ["name"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_products_name"), "products", ["name"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("entity", sa.String(), nullable=True),
        sa.Column("entity_id", sa.String(), nullable=True),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "doctors",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("specialization", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("hospital_id", sa.String(), nullable=True),
        sa.Column("created_by", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["hospital_id"], ["hospitals.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_doctors_name"), "doctors", ["name"], unique=False)

    op.create_table(
        "notifications",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("is_read", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "interactions",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("doctor_id", sa.String(), nullable=False),
        sa.Column("rep_id", sa.String(), nullable=False),
        sa.Column("meeting_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("meeting_type", meeting_type, nullable=True),
        sa.Column("products_discussed", sa.String(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("samples_given", sa.Boolean(), nullable=True),
        sa.Column("priority", priority, nullable=True),
        sa.Column("follow_up_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attachment_url", sa.String(), nullable=True),
        sa.Column("ai_summary", sa.Text(), nullable=True),
        sa.Column("ai_action_items", sa.Text(), nullable=True),
        sa.Column("source", interaction_source, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["doctor_id"], ["doctors.id"]),
        sa.ForeignKeyConstraint(["rep_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "followups",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("interaction_id", sa.String(), nullable=False),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_completed", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(["interaction_id"], ["interactions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("followups")
    op.drop_table("interactions")
    op.drop_table("notifications")
    op.drop_index(op.f("ix_doctors_name"), table_name="doctors")
    op.drop_table("doctors")
    op.drop_table("audit_logs")
    op.drop_index(op.f("ix_products_name"), table_name="products")
    op.drop_table("products")
    op.drop_index(op.f("ix_hospitals_name"), table_name="hospitals")
    op.drop_table("hospitals")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")

    bind = op.get_bind()
    interaction_source.drop(bind, checkfirst=True)
    priority.drop(bind, checkfirst=True)
    meeting_type.drop(bind, checkfirst=True)
    user_role.drop(bind, checkfirst=True)
