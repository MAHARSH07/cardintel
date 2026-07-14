"""User routes will be added with authentication and onboarding."""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])
