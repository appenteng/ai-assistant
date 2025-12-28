"""
Travel Service - Basic version
"""
from typing import Dict, List
import random

class TravelService:
    def __init__(self):
        self.destinations = {
            "beach": ["Bali", "Maldives", "Hawaii"],
            "city": ["Paris", "Tokyo", "New York"],
            "mountain": ["Swiss Alps", "Rocky Mountains"]
        }

    def plan_trip(self, destination: str, days: int) -> Dict:
        """Basic trip planning"""
        return {
            "destination": destination,
            "days": days,
            "itinerary": [f"Day {i+1}: Explore {destination}" for i in range(days)],
            "estimated_cost": days * 150
        }

    def get_popular_destinations(self) -> Dict[str, List[str]]:
        """Get popular destinations"""
        return self.destinations
