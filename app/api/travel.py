from fastapi import APIRouter
from app.services.travel_service import TravelService

router = APIRouter()
travel_service = TravelService()

@router.get("/plan")
def plan_trip(destination: str = "Paris", days: int = 3):
    """Plan a trip"""
    plan = travel_service.plan_trip(destination, days)
    return plan