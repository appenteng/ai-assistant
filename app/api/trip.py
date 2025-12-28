# backend/app/api/trips.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.trip import TripCreate, TripResponse, TripHistoryResponse, TripUpdate
from app.services.trip_service import TripService
from app.services.travel_service import TravelService

router = APIRouter()


@router.post("/", response_model=TripResponse)
async def create_trip(
        trip_data: TripCreate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Save a new trip to user's history"""
    return TripService.create_trip(db, current_user.id, trip_data)


@router.get("/", response_model=TripHistoryResponse)
async def get_trips(
        page: int = Query(1, ge=1),
        limit: int = Query(10, ge=1, le=100),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Get user's trip history with pagination"""
    skip = (page - 1) * limit
    trips = TripService.get_user_trips(db, current_user.id, skip, limit)
    total = db.query(Trip).filter(Trip.user_id == current_user.id).count()

    return {
        "trips": trips,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": (total + limit - 1) // limit
        }
    }


@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(
        trip_id: str,
        updates: TripUpdate,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """Update a trip"""
    trip = TripService.update_trip(db, trip_id, current_user.id, updates)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip