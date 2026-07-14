"""Admin routes will be added with catalogue administration."""

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])
