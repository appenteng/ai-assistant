# app/api/router.py
from fastapi import APIRouter
from app.api.main import router as main_router
from app.api.travel import router as travel_router
from app.api.chat import router as chat_router  # ADD THIS LINE

api_router = APIRouter()

api_router.include_router(main_router, tags=["main"])
api_router.include_router(travel_router, prefix="/travel", tags=["travel"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])  # ADD THIS LINE