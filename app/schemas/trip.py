from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid


class TripBase(BaseModel):
    title: str
    destination: str
    start_date: datetime
    end_date: datetime
    total_budget: float = 0


class TripCreate(TripBase):
    itinerary: Dict[str, Any] = {}
    preferences: Dict[str, Any] = {}


class TripUpdate(BaseModel):
    title: Optional[str] = None
    itinerary: Optional[Dict[str, Any]] = None
    preferences: Optional[Dict[str, Any]] = None


class TripResponse(TripBase):
    id: uuid.UUID
    user_id: uuid.UUID
    itinerary: Dict[str, Any]
    preferences: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TripHistoryResponse(BaseModel):
    trips: List[TripResponse]
    pagination: Dict[str, Any]