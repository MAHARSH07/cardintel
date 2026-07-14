"""Recommendation routes will be added when ranking is implemented."""

from fastapi import APIRouter

router = APIRouter(prefix="/recommendations", tags=["recommendations"])
