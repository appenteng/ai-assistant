# backend/app/services/trip_service.py
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.trip import Trip
from app.schemas.trip import TripCreate, TripUpdate
import uuid


class TripService:
    @staticmethod
    def create_trip(
            db: Session,
            user_id: uuid.UUID,
            trip_data: TripCreate
    ) -> Trip:
        """Create a new trip for user"""
        trip = Trip(
            user_id=user_id,
            **trip_data.dict()
        )
        db.add(trip)
        db.commit()
        db.refresh(trip)
        return trip

    @staticmethod
    def get_user_trips(
            db: Session,
            user_id: uuid.UUID,
            skip: int = 0,
            limit: int = 100
    ) -> List[Trip]:
        """Get all trips for a user"""
        return db.query(Trip) \
            .filter(Trip.user_id == user_id) \
            .order_by(Trip.created_at.desc()) \
            .offset(skip) \
            .limit(limit) \
            .all()

    @staticmethod
    def update_trip(
            db: Session,
            trip_id: uuid.UUID,
            user_id: uuid.UUID,
            updates: TripUpdate
    ) -> Optional[Trip]:
        """Update a trip"""
        trip = db.query(Trip) \
            .filter(Trip.id == trip_id, Trip.user_id == user_id) \
            .first()

        if not trip:
            return None

        update_data = updates.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(trip, field, value)

        db.commit()
        db.refresh(trip)
        return trip