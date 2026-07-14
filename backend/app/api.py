from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models import User
from app.schemas import CardSearchQuery, LoginRequest, RecommendationRequest, RegisterRequest, TokenResponse

router = APIRouter()


@router.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, tags=["auth"])
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> TokenResponse:
    existing_user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing_user:
        raise HTTPException(status_code=409, detail="Email is already registered")
    user = User(email=payload.email.lower(), password_hash=hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(str(user.id), user.role.value))


@router.post("/auth/login", response_model=TokenResponse, tags=["auth"])
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return TokenResponse(access_token=create_access_token(str(user.id), user.role.value))


@router.get("/cards", tags=["cards"])
def search_cards(filters: CardSearchQuery = Depends()) -> dict:
    """Search endpoint contract; persistent card querying follows the initial card migration."""
    return {"items": [], "filters": filters.model_dump(exclude_none=True)}


@router.post("/recommendations", tags=["recommendations"])
def recommend_cards(payload: RecommendationRequest) -> dict:
    """Recommendation endpoint contract; ranking is added once card data is ingested."""
    return {"items": [], "input": payload.model_dump()}
