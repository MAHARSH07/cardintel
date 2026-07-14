"""Admin routes will be added with administration workflows."""

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])
