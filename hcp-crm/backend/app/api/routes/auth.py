"""Authentication routes: register, login."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserOut, Token
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


def authenticate_user(db: Session, email: str, password: str) -> User:
    """Validate credentials and return the user, or raise 401."""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    return user


@router.post("/register", response_model=UserOut)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        full_name=payload.full_name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    token = create_access_token(subject=user.email)
    return Token(access_token=token, user=user)


@router.post("/login-json", response_model=Token)
def login_json(payload: UserLogin, db: Session = Depends(get_db)):
    """JSON login used by the React frontend (axios) instead of form-encoded."""
    user = authenticate_user(db, payload.email, payload.password)
    token = create_access_token(subject=user.email)
    return Token(access_token=token, user=user)
