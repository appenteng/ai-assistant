# backend/app/models/user.py
from sqlalchemy import Column, String, Boolean, JSON
from .base import Base


class User(Base):
    __tablename__ = "users"

    # ... existing columns ...

    # Add preferences column
    preferences = Column(JSON, default={
        "budget_range": {"min": 0, "max": 10000},
        "travel_style": ["cultural", "relaxation"],
        "dietary_restrictions": [],
        "accessibility_needs": False,
        "preferred_accommodation": ["hotel", "airbnb"],
        "preferred_transport": ["flight", "train"],
        "activities": ["sightseeing", "food", "shopping"],
        "climate_preference": "moderate"
    })