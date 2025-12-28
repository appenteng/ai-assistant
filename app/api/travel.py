# app/api/travel.py
from fastapi import APIRouter, HTTPException, Query
from app.services.travel_service import TravelService
from typing import Optional, List
import json

router = APIRouter()
travel_service = TravelService()


@router.get("/plan")
async def plan_trip(
        destination: str = Query("Paris", description="Destination name"),
        days: int = Query(3, ge=1, le=30, description="Number of days (1-30)"),
        budget: Optional[float] = Query(None, description="Optional budget constraint")
):
    """Plan and save a trip"""
    try:
        # Get plan from service
        plan = travel_service.plan_trip(destination, days)

        if not plan.get("saved", False):
            raise HTTPException(status_code=500, detail="Failed to save trip to database")

        # Check if within budget if provided
        if budget is not None:
            plan["within_budget"] = plan["estimated_cost"] <= budget
            plan["budget_difference"] = budget - plan["estimated_cost"]

        return {
            "status": "success",
            "message": f"Trip to {destination} planned successfully",
            "trip_id": plan.get("trip_id"),
            "plan": plan
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/recent")
def get_recent_trips(limit: int = Query(5, ge=1, le=50, description="Number of trips to fetch")):
    """Get recent trips from database"""
    trips = travel_service.get_recent_trips(limit)
    return {
        "count": len(trips),
        "trips": trips
    }


@router.get("/destinations")
def get_popular_destinations():
    """Get categorized popular destinations"""
    return travel_service.get_popular_destinations()


@router.get("/trip/{trip_id}")
def get_trip_by_id(trip_id: int):
    """Get specific trip by ID"""
    trip = travel_service.get_trip_by_id(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip