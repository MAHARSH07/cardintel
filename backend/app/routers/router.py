from fastapi import APIRouter

from app.routers.banks import admin_router as admin_bank_router
from app.routers.banks import public_router as bank_router
from app.routers.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(bank_router)
api_router.include_router(admin_bank_router)
