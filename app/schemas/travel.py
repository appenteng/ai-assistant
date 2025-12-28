"""
Travel schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import date

class TravelRequest(BaseModel):
    destination: str
    budget: float
    start_date: date
    end_date: date
    travelers: int = 1
    preferences: Optional[Dict] = None

class TravelResponse(BaseModel):
    status: str
    itinerary: Dict
    bookings: List[Dict]
    summary: str