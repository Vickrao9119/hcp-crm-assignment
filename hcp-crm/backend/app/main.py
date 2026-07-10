"""
FastAPI application entrypoint.

Wires up CORS, routers, and (in dev) auto-creates tables so the app runs
without requiring an Alembic migration step first. In production, use
`alembic upgrade head` instead of relying on create_all.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import Base, engine, wait_for_postgres
from app.models import *  # noqa: F401,F403 — ensures all models are registered
from app.api.routes import auth, doctors, interactions, chat, dashboard, notifications, users

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(doctors.router)
app.include_router(interactions.router)
app.include_router(chat.router)
app.include_router(dashboard.router)
app.include_router(notifications.router)
app.include_router(users.router)


@app.on_event("startup")
def on_startup():
    wait_for_postgres()
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "ok", "service": settings.PROJECT_NAME}


@app.get("/health")
def health():
    return {"status": "healthy"}
