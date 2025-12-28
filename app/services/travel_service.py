# app/services/travel_service.py - ENHANCED VERSION
import json
from typing import Dict, List

class TravelService:
    def __init__(self):
        self.popular_destinations = {
            "beach": ["Hawaii", "Bali", "Maldives", "Thailand", "Bahamas"],
            "city": ["Paris", "Tokyo", "New York", "London", "Dubai"],
            "mountain": ["Swiss Alps", "Rocky Mountains", "Andes", "Himalayas", "Alps"],
            "adventure": ["New Zealand", "Costa Rica", "Iceland", "Norway", "Canada"]
        }
        
        self.activity_templates = {
            "beach": ["Sunbathe", "Swim", "Snorkel", "Beach volleyball", "Sunset cruise"],
            "city": ["Museum tour", "Local cuisine", "Shopping", "Historical sites", "Nightlife"],
            "mountain": ["Hiking", "Photography", "Wildlife spotting", "Camping", "Stargazing"],
            "adventure": ["Zip-lining", "Whitewater rafting", "Bungee jumping", "Safari", "Helicopter tour"]
        }
    
    def plan_trip(self, destination: str, days: int) -> Dict:
        """Create detailed trip plan"""
        trip_type = self._determine_trip_type(destination)
        
        return {
            "destination": destination,
            "days": days,
            "trip_type": trip_type,
            "itinerary": self._create_itinerary(destination, days, trip_type),
            "estimated_cost": self._calculate_costs(days, trip_type)["total"],
            "cost_breakdown": self._calculate_costs(days, trip_type),
            "recommendations": self._get_recommendations(destination, trip_type),
            "packing_list": self._get_packing_list(trip_type, days)
        }
    
    def _determine_trip_type(self, destination: str) -> str:
        destination_lower = destination.lower()
        if any(word in destination_lower for word in ["beach", "island", "coast", "sea"]):
            return "beach"
        elif any(word in destination_lower for word in ["mountain", "alps", "peak", "hike"]):
            return "mountain"
        elif any(word in destination_lower for word in ["adventure", "safari", "wild", "explore"]):
            return "adventure"
        else:
            return "city"
    
    def _create_itinerary(self, destination: str, days: int, trip_type: str) -> List[str]:
        activities = self.activity_templates.get(trip_type, self.activity_templates["city"])
        
        itinerary = []
        for day in range(1, days + 1):
            if day == 1:
                itinerary.append(f"Day {day}: Arrive in {destination}, check-in, explore")
            elif day == days:
                itinerary.append(f"Day {day}: Last-minute shopping, souvenirs, departure")
            else:
                activity_idx = (day - 2) % len(activities)
                itinerary.append(f"Day {day}: {activities[activity_idx]} in {destination}")
        
        return itinerary
    
    def _calculate_costs(self, days: int, trip_type: str) -> Dict:
        cost_per_day = {"beach": 200, "city": 180, "mountain": 150, "adventure": 250}
        daily = cost_per_day.get(trip_type, 150)
        
        return {
            "accommodation": days * (daily * 0.4),
            "food": days * (daily * 0.3),
            "activities": days * (daily * 0.2),
            "transportation": days * (daily * 0.1),
            "total": days * daily
        }
    
    def get_popular_destinations(self) -> Dict[str, List[str]]:
        return self.popular_destinations