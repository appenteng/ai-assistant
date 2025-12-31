import httpx
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import os
import random


class HotelService:
    def __init__(self):
        self.api_key = os.getenv("BOOKING_API_KEY", "mock-key")
        self.use_mock = self.api_key == "mock-key"

    async def search_hotels(
            self,
            location: str,
            check_in: str,
            check_out: str,
            guests: int = 2,
            rooms: int = 1,
            sort_by: str = "popularity"
    ) -> Dict:
        """Search hotels using Booking.com API"""

        if self.use_mock:
            return self._mock_hotel_search(location, check_in, check_out, guests)

        # Real API implementation
        try:
            url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
            }

            params = {
                "checkin_date": check_in,
                "checkout_date": check_out,
                "units": "metric",
                "dest_id": location,
                "dest_type": "city",
                "adults_number": str(guests),
                "order_by": sort_by,
                "filter_by_currency": "USD",
                "locale": "en-us",
                "room_number": str(rooms)
            }

            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
                response.raise_for_status()
                return response.json()

        except Exception as e:
            print(f"Hotel API error: {e}")
            return self._mock_hotel_search(location, check_in, check_out, guests)

    def _mock_hotel_search(
            self,
            location: str,
            check_in: str,
            check_out: str,
            guests: int = 2
    ) -> Dict:
        """Mock hotel data for development"""
        hotels = []

        hotel_names = [
            "Grand Luxury Hotel",
            "City Center Inn",
            "Seaside Resort",
            "Mountain View Lodge",
            "Business Plaza Hotel",
            "Boutique Urban Stay",
            "Traditional Heritage Inn"
        ]

        locations = ["Downtown", "City Center", "Waterfront", "Business District", "Historic District"]

        for i in range(7):
            price_per_night = random.randint(120, 400)
            total_nights = 3  # Mock calculation
            total_price = price_per_night * total_nights

            hotels.append({
                "id": f"HT{i + 1:03d}",
                "name": f"{hotel_names[i]} {location}",
                "location": f"{location}, {random.choice(locations)}",
                "description": f"Beautiful hotel in the heart of {location} with amazing amenities.",
                "rating": round(random.uniform(3.5, 5.0), 1),
                "review_count": random.randint(50, 2000),
                "price_per_night": price_per_night,
                "total_price": total_price,
                "currency": "USD",
                "amenities": [
                    "Free WiFi",
                    "Swimming Pool",
                    "Fitness Center",
                    "Restaurant",
                    "Spa",
                    "Parking" if i % 2 == 0 else None
                ],
                "room_type": random.choice(["Deluxe King", "Standard Double", "Executive Suite", "Family Room"]),
                "available_rooms": random.randint(5, 20),
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests,
                "images": [
                    f"https://example.com/hotel{i + 1}_1.jpg",
                    f"https://example.com/hotel{i + 1}_2.jpg"
                ],
                "booking_link": f"https://example.com/book/hotel/{i + 1}"
            })

        return {
            "status": "success",
            "location": location,
            "check_in": check_in,
            "check_out": check_out,
            "total_hotels": len(hotels),
            "lowest_price": min(h["price_per_night"] for h in hotels),
            "hotels": sorted(hotels, key=lambda x: x["price_per_night"])
        }

    async def get_hotel_details(self, hotel_id: str) -> Optional[Dict]:
        """Get detailed hotel information"""
        # Mock implementation
        return {
            "id": hotel_id,
            "name": f"Sample Hotel {hotel_id}",
            "description": "A wonderful place to stay with excellent service.",
            "full_details": {
                "check_in_time": "3:00 PM",
                "check_out_time": "11:00 AM",
                "policies": ["Free cancellation", "Breakfast included"],
                "reviews": [
                    {"user": "Traveler123", "rating": 5, "comment": "Excellent stay!"},
                    {"user": "AdventureSeeker", "rating": 4, "comment": "Great location"}
                ]
            }
        }