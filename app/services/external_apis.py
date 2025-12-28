# backend/app/services/external_apis.py
import aiohttp
import os
from typing import Optional, Dict, Any, List
from datetime import datetime


class FlightAPIService:
    def __init__(self):
        self.api_key = os.getenv("RAPIDAPI_KEY")
        self.base_url = "https://skyscanner-api.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "skyscanner-api.p.rapidapi.com"
        }

    async def search_flights(
            self,
            origin: str,
            destination: str,
            departure_date: str,
            return_date: Optional[str] = None,
            adults: int = 1
    ) -> List[Dict[str, Any]]:
        """Search for flights using Skyscanner API"""
        async with aiohttp.ClientSession() as session:
            params = {
                "origin": origin,
                "destination": destination,
                "departure_date": departure_date,
                "adults": adults
            }
            if return_date:
                params["return_date"] = return_date

            async with session.get(
                    f"{self.base_url}/flights/search",
                    headers=self.headers,
                    params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_flight_results(data)
                else:
                    return []


class HotelAPIService:
    async def search_hotels(
            self,
            location: str,
            check_in: str,
            check_out: str,
            guests: int = 1
    ) -> List[Dict[str, Any]]:
        """Search for hotels"""
        # Implement similar API integration
        pass