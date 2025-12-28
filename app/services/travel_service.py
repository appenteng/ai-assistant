# app/services/travel_service.py - DATABASE VERSION
import json
from typing import Dict, List, Optional
from datetime import datetime
from app.core.database import SessionLocal
from app.models.trip import Trip


class TravelService:
    def __init__(self):
        self.popular_destinations = {
            "beach": ["Hawaii", "Bali", "Maldives", "Thailand", "Bahamas"],
            "city": ["Paris", "Tokyo", "New York", "London", "Dubai"],
            "mountain": ["Swiss Alps", "Rocky Mountains", "Andes", "Himalayas"],
            "adventure": ["New Zealand", "Costa Rica", "Iceland", "Norway"]
        }

    def plan_trip(self, destination: str, days: int, user_id: Optional[int] = None) -> Dict:
        """Create and save trip plan to database"""
        # 1. Create the plan
        plan = self._create_plan(destination, days)

        # 2. Save to database
        db = SessionLocal()
        try:
            trip = Trip(
                user_id=user_id,
                destination=destination,
                days=days,
                budget=plan["estimated_cost"],
                itinerary=json.dumps(plan["itinerary"]),
                preferences={
                    "type": plan["trip_type"],
                    "cost_level": plan["cost_level"],
                    "activities": plan["recommendations"]
                }
            )

            db.add(trip)
            db.commit()
            db.refresh(trip)

            # Add database ID to response
            plan["trip_id"] = trip.id
            plan["saved"] = True
            plan["created_at"] = trip.created_at.isoformat() if trip.created_at else None

        except Exception as e:
            plan["saved"] = False
            plan["error"] = str(e)
            print(f"❌ Error saving trip: {e}")
        finally:
            db.close()

        return plan

    def get_recent_trips(self, limit: int = 10) -> List[Dict]:
        """Get recent trips from database"""
        db = SessionLocal()
        try:
            trips = db.query(Trip).order_by(Trip.created_at.desc()).limit(limit).all()
            return [trip.to_dict() for trip in trips]
        except Exception as e:
            print(f"❌ Error fetching trips: {e}")
            return []
        finally:
            db.close()

    def get_trip_by_id(self, trip_id: int) -> Optional[Dict]:
        """Get specific trip by ID"""
        db = SessionLocal()
        try:
            trip = db.query(Trip).filter(Trip.id == trip_id).first()
            return trip.to_dict() if trip else None
        finally:
            db.close()

    def _create_plan(self, destination: str, days: int) -> Dict:
        """Create detailed trip plan"""
        trip_type = self._determine_trip_type(destination)

        # Create itinerary
        itinerary = []
        for day in range(1, days + 1):
            if day == 1:
                itinerary.append(f"Day {day}: Arrive in {destination}, check into accommodation, explore local area")
            elif day == days:
                itinerary.append(f"Day {day}: Last-minute shopping, souvenir hunting, departure from {destination}")
            else:
                activity = self._get_activity_for_day(trip_type, day)
                itinerary.append(f"Day {day}: {activity} in {destination}")

        # Calculate costs
        cost_data = self._calculate_costs(days, trip_type)

        return {
            "destination": destination,
            "days": days,
            "trip_type": trip_type,
            "itinerary": itinerary,
            "estimated_cost": cost_data["total"],
            "cost_breakdown": cost_data,
            "cost_level": self._get_cost_level(cost_data["total"]),
            "recommendations": self._get_recommendations(trip_type),
            "packing_tips": self._get_packing_tips(trip_type, days)
        }

    def _determine_trip_type(self, destination: str) -> str:
        """Determine type of trip based on destination keywords"""
        destination_lower = destination.lower()

        beach_keywords = ["beach", "island", "coast", "sea", "ocean", "shore", "tropical"]
        mountain_keywords = ["mountain", "alps", "peak", "hike", "ski", "snow", "summit"]
        adventure_keywords = ["adventure", "safari", "wild", "explore", "jungle", "desert"]

        if any(keyword in destination_lower for keyword in beach_keywords):
            return "beach"
        elif any(keyword in destination_lower for keyword in mountain_keywords):
            return "mountain"
        elif any(keyword in destination_lower for keyword in adventure_keywords):
            return "adventure"
        else:
            return "city"

    def _get_activity_for_day(self, trip_type: str, day: int) -> str:
        """Get activity based on trip type"""
        activities = {
            "beach": ["Sunbathe and relax", "Try water sports", "Go snorkeling", "Take a boat tour", "Watch sunset"],
            "city": ["Visit museums", "Try local cuisine", "Go shopping", "Explore historical sites",
                     "Experience nightlife"],
            "mountain": ["Go hiking", "Take photos", "Watch wildlife", "Camp under stars", "Visit viewpoints"],
            "adventure": ["Try zip-lining", "Go rafting", "Take a safari", "Explore caves", "Try local adventures"]
        }
        default_activities = activities.get(trip_type,
                                            ["Explore the area", "Try local experiences", "Visit attractions"])

        activity_index = (day - 2) % len(default_activities)
        return default_activities[activity_index]

    def _calculate_costs(self, days: int, trip_type: str) -> Dict:
        """Calculate estimated costs"""
        base_costs = {
            "beach": {"daily": 200, "accommodation_pct": 0.4, "food_pct": 0.3, "activities_pct": 0.2,
                      "transport_pct": 0.1},
            "city": {"daily": 180, "accommodation_pct": 0.45, "food_pct": 0.35, "activities_pct": 0.15,
                     "transport_pct": 0.05},
            "mountain": {"daily": 150, "accommodation_pct": 0.3, "food_pct": 0.25, "activities_pct": 0.35,
                         "transport_pct": 0.1},
            "adventure": {"daily": 250, "accommodation_pct": 0.35, "food_pct": 0.25, "activities_pct": 0.3,
                          "transport_pct": 0.1}
        }

        costs = base_costs.get(trip_type, base_costs["city"])
        daily = costs["daily"]
        total = days * daily

        return {
            "accommodation": round(total * costs["accommodation_pct"], 2),
            "food": round(total * costs["food_pct"], 2),
            "activities": round(total * costs["activities_pct"], 2),
            "transportation": round(total * costs["transport_pct"], 2),
            "total": round(total, 2)
        }

    def _get_cost_level(self, total_cost: float) -> str:
        """Determine cost level"""
        if total_cost < 500:
            return "budget"
        elif total_cost < 1500:
            return "moderate"
        elif total_cost < 3000:
            return "luxury"
        else:
            return "premium"

    def _get_recommendations(self, trip_type: str) -> List[str]:
        """Get trip-type specific recommendations"""
        recommendations = {
            "beach": ["Apply sunscreen regularly", "Stay hydrated", "Try local seafood", "Watch sunrise/sunset"],
            "city": ["Use public transport", "Try street food", "Learn basic phrases", "Mix tourist/local spots"],
            "mountain": ["Dress in layers", "Carry water/snacks", "Check weather", "Tell someone your plans"],
            "adventure": ["Get travel insurance", "Check equipment", "Follow guides", "Know your limits"]
        }
        return recommendations.get(trip_type, ["Enjoy your trip!", "Take lots of photos"])

    def _get_packing_tips(self, trip_type: str, days: int) -> List[str]:
        """Get packing tips"""
        base = ["Passport/ID", "Phone charger", "Medications", "Travel documents", "Cash/cards"]

        type_specific = {
            "beach": ["Swimwear", "Sunglasses", "Beach towel", "Sandals", "Hat", "Sunscreen"],
            "city": ["Comfortable shoes", "City map/app", "Day bag", "Light jacket", "Power bank"],
            "mountain": ["Hiking boots", "Warm layers", "Water bottle", "First aid kit", "Backpack"],
            "adventure": ["Sturdy shoes", "Quick-dry clothes", "Waterproof bag", "Multi-tool", "Headlamp"]
        }

        return base + type_specific.get(trip_type, [])

    def get_popular_destinations(self) -> Dict[str, List[str]]:
        """Get categorized popular destinations"""
        return self.popular_destinations