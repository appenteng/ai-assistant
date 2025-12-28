# app/api/user.py
from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

@router.get("/dashboard")
async def get_user_dashboard(current_user: User = Depends(get_current_user)):
    """Get user dashboard data"""
    # TODO: Get real stats from database
    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username
        },
        "stats": {
            "trips_planned": 0,
            "total_spent": 0,
            "hours_saved": 0,
            "favorite_destination": None
        },
        "recent_trips": [],
        "recommendations": [
            "Try planning a trip to Japan",
            "Complete your profile",
            "Set up travel preferences"
        ]
    }

@router.get("/trips")
async def get_user_trips(current_user: User = Depends(get_current_user)):
    """Get user's trip history"""
    # TODO: Get trips from database
    return {
        "user_id": current_user.id,
        "trips": [],
        "count": 0,
        "message": "No trips found. Plan your first trip!"
    }

@router.get("/preferences")
async def get_user_preferences(current_user: User = Depends(get_current_user)):
    """Get user preferences"""
    return {
        "user_id": current_user.id,
        "preferences": current_user.preferences or {}
    }

@router.put("/preferences")
async def update_user_preferences(
    preferences: dict,
    current_user: User = Depends(get_current_user)
):
    """Update user preferences"""
    # TODO: Update in database
    return {
        "success": True,
        "message": "Preferences updated",
        "preferences": preferences
    }