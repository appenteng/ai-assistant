from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.hotel_service import HotelService

router = APIRouter(prefix="/hotels", tags=["Hotels"])
hotel_service = HotelService()


@router.get("/search")
async def search_hotels(
        location: str = Query(..., description="City or destination name"),
        check_in: str = Query(..., description="Check-in date (YYYY-MM-DD)"),
        check_out: str = Query(..., description="Check-out date (YYYY-MM-DD)"),
        guests: int = Query(2, ge=1, le=10),
        rooms: int = Query(1, ge=1, le=5),
        sort_by: str = Query("popularity", regex="^(popularity|price|distance|rating)$")
):
    """Search for hotels in a location"""
    try:
        results = await hotel_service.search_hotels(
            location=location,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            rooms=rooms,
            sort_by=sort_by
        )

        if results.get("status") == "error":
            raise HTTPException(status_code=400, detail=results.get("message", "Hotel search failed"))

        return {
            "success": True,
            "data": results,
            "search_params": {
                "location": location,
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests,
                "rooms": rooms
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hotel search error: {str(e)}")


@router.get("/{hotel_id}")
async def get_hotel_details(hotel_id: str):
    """Get detailed hotel information"""
    hotel = await hotel_service.get_hotel_details(hotel_id)

    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return {
        "success": True,
        "hotel": hotel
    }


@router.get("/popular-destinations")
async def get_popular_hotel_destinations():
    """Get popular hotel destinations"""
    popular_destinations = [
        {"city": "Paris", "country": "France", "avg_price": 180, "hotel_count": 1250},
        {"city": "Tokyo", "country": "Japan", "avg_price": 150, "hotel_count": 980},
        {"city": "New York", "country": "USA", "avg_price": 250, "hotel_count": 2100},
        {"city": "Dubai", "country": "UAE", "avg_price": 220, "hotel_count": 850},
        {"city": "Bali", "country": "Indonesia", "avg_price": 120, "hotel_count": 750},
    ]

    return {
        "success": True,
        "destinations": popular_destinations
    }