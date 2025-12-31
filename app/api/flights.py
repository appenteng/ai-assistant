from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
from app.services.flight_service import FlightService
from datetime import datetime, timedelta

router = APIRouter(prefix="/flights", tags=["Flights"])
flight_service = FlightService()


@router.get("/search")
async def search_flights(
        origin: str = Query(..., description="Departure airport code (e.g., JFK)"),
        destination: str = Query(..., description="Arrival airport code (e.g., LAX)"),
        departure_date: str = Query(..., description="Departure date (YYYY-MM-DD)"),
        return_date: Optional[str] = Query(None, description="Return date (YYYY-MM-DD)"),
        adults: int = Query(1, ge=1, le=9),
        cabin_class: str = Query("economy", regex="^(economy|premium|business|first)$")
):
    """Search for flights between airports"""
    try:
        results = await flight_service.search_flights(
            origin=origin,
            destination=destination,
            departure_date=departure_date,
            return_date=return_date,
            adults=adults,
            cabin_class=cabin_class
        )

        if results.get("status") == "error":
            raise HTTPException(status_code=400, detail=results.get("message", "Flight search failed"))

        return {
            "success": True,
            "data": results,
            "search_params": {
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "return_date": return_date,
                "travelers": adults,
                "class": cabin_class
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Flight search error: {str(e)}")


@router.get("/airports")
async def search_airports(query: str = Query(..., min_length=2, description="Search by city, airport name, or code")):
    """Search airports by name, city, or code"""
    airports = await flight_service.get_airports(query)

    return {
        "success": True,
        "query": query,
        "count": len(airports),
        "airports": airports[:10]  # Limit results
    }


@router.get("/popular-routes")
async def get_popular_routes():
    """Get popular flight routes"""
    popular_routes = [
        {"origin": "JFK", "destination": "LAX", "avg_price": 350, "popularity": "High"},
        {"origin": "LHR", "destination": "JFK", "avg_price": 600, "popularity": "High"},
        {"origin": "CDG", "destination": "FCO", "avg_price": 150, "popularity": "Medium"},
        {"origin": "HND", "destination": "ICN", "avg_price": 280, "popularity": "Medium"},
        {"origin": "SYD", "destination": "AKL", "avg_price": 220, "popularity": "Low"},
    ]

    return {
        "success": True,
        "routes": popular_routes
    }