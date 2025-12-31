import httpx
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os
from app.core.config import settings


class FlightService:
    def __init__(self):
        self.api_key = os.getenv("SKYSCANNER_API_KEY", "mock-key")
        self.use_mock = self.api_key == "mock-key"

    async def search_flights(
            self,
            origin: str,
            destination: str,
            departure_date: str,
            return_date: Optional[str] = None,
            adults: int = 1,
            cabin_class: str = "economy"
    ) -> Dict:
        """Search for flights using Skyscanner API"""

        if self.use_mock:
            return self._mock_flight_search(origin, destination, departure_date, return_date)

        # Real API implementation
        try:
            url = "https://skyscanner-api.p.rapidapi.com/v3/flights/live/search"

            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "skyscanner-api.p.rapidapi.com"
            }

            payload = {
                "query": {
                    "market": "US",
                    "locale": "en-US",
                    "currency": "USD",
                    "queryLegs": [
                        {
                            "originPlaceId": {"iata": origin.upper()},
                            "destinationPlaceId": {"iata": destination.upper()},
                            "date": {"year": 2024, "month": 6, "day": 15}
                        }
                    ],
                    "cabinClass": cabin_class.lower(),
                    "adults": adults
                }
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers, timeout=30.0)
                response.raise_for_status()
                return response.json()

        except Exception as e:
            print(f"Flight API error: {e}")
            return self._mock_flight_search(origin, destination, departure_date, return_date)

    def _mock_flight_search(
            self,
            origin: str,
            destination: str,
            departure_date: str,
            return_date: Optional[str] = None
    ) -> Dict:
        """Mock flight data for development"""
        flights = []

        airlines = ["Delta", "American Airlines", "United", "Southwest", "JetBlue"]
        prices = [299.99, 349.99, 279.99, 319.99, 259.99]

        for i in range(5):
            departure_time = f"{departure_date}T{8 + i}:00:00"
            arrival_time = f"{departure_date}T{11 + i}:00:00"

            flights.append({
                "id": f"FL{i + 1:03d}",
                "airline": airlines[i],
                "flight_number": f"{airlines[i][:2].upper()}{100 + i}",
                "origin": origin.upper(),
                "destination": destination.upper(),
                "departure_time": departure_time,
                "arrival_time": arrival_time,
                "duration": "3h 00m",
                "stops": 0 if i < 3 else 1,
                "cabin_class": "economy",
                "price": prices[i],
                "currency": "USD",
                "available_seats": 150 - (i * 20),
                "booking_link": f"https://example.com/book/flight/{i + 1}"
            })

        return {
            "status": "success",
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "total_flights": len(flights),
            "cheapest_price": min(f["price"] for f in flights),
            "flights": flights
        }

    async def get_airports(self, query: str) -> List[Dict]:
        """Search airports by city/name"""
        mock_airports = [
            {"code": "JFK", "name": "John F Kennedy International", "city": "New York", "country": "USA"},
            {"code": "LAX", "name": "Los Angeles International", "city": "Los Angeles", "country": "USA"},
            {"code": "LHR", "name": "London Heathrow", "city": "London", "country": "UK"},
            {"code": "CDG", "name": "Charles de Gaulle", "city": "Paris", "country": "France"},
            {"code": "HND", "name": "Tokyo Haneda", "city": "Tokyo", "country": "Japan"},
            {"code": "DXB", "name": "Dubai International", "city": "Dubai", "country": "UAE"},
            {"code": "SYD", "name": "Sydney Kingsford Smith", "city": "Sydney", "country": "Australia"},
        ]

        query_lower = query.lower()
        return [ap for ap in mock_airports
                if query_lower in ap["city"].lower()
                or query_lower in ap["name"].lower()
                or query_lower in ap["code"].lower()]