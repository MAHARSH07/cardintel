"""Card routes will be added with the card catalogue module."""

from fastapi import APIRouter

router = APIRouter(prefix="/cards", tags=["cards"])
