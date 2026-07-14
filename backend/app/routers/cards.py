"""Card catalogue routes will be added after bank management."""

from fastapi import APIRouter

router = APIRouter(prefix="/cards", tags=["cards"])
