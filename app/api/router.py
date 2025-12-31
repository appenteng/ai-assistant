
from fastapi import APIRouter
from app.api.main import router as main_router
from app.api.auth import router as auth_router
from app.api.travel import router as travel_router

api_router = APIRouter()
api_router.include_router(main_router, tags=["main"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(travel_router, prefix="/travel", tags=["travel"])
