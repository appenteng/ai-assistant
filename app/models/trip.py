# backend/app/models/trip.py
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, DECIMAL, UUID
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .base import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    title = Column(String(255))
    destination = Column(String(255))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_budget = Column(DECIMAL(10, 2), default=0)
    itinerary = Column(JSON)  # Store AI-generated itinerary
    preferences = Column(JSON)  # Preferences used for this trip
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())