# app/models/trip.py
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base
import json


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=True)
    destination = Column(String, nullable=False)
    days = Column(Integer, default=3)
    budget = Column(Float, default=1000.0)
    itinerary = Column(Text)  # JSON stored as text
    preferences = Column(JSON, default={})
    status = Column(String, default="planned")  # planned, booked, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def to_dict(self):
        """Convert to dictionary for API response"""
        try:
            itinerary_data = json.loads(self.itinerary) if self.itinerary else []
        except:
            itinerary_data = []

        return {
            "id": self.id,
            "user_id": self.user_id,
            "destination": self.destination,
            "days": self.days,
            "budget": self.budget,
            "itinerary": itinerary_data,
            "preferences": self.preferences,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }