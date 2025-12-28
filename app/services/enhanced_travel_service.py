# backend/app/services/enhanced_travel_service.py
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.services.openai_service import OpenAIService


class EnhancedTravelService:
    def __init__(self):
        self.openai_service = OpenAIService()

    async def create_intelligent_itinerary(
            self,
            destination: str,
            days: int,
            budget: float,
            preferences: Dict[str, Any],
            travel_dates: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """Create AI-optimized itinerary considering multiple factors"""

        # Prepare context for AI
        context = {
            "destination": destination,
            "duration_days": days,
            "total_budget": budget,
            "preferences": preferences,
            "travel_dates": travel_dates,
            "current_season": self._get_season(travel_dates[0] if travel_dates else datetime.now()),
            "budget_per_day": budget / days if days > 0 else budget
        }

        # Use AI to create optimized itinerary
        prompt = self._build_itinerary_prompt(context)
        response = await self.openai_service.get_completion(prompt)

        # Parse and structure the response
        itinerary = self._parse_itinerary_response(response, context)

        # Optimize budget allocation
        itinerary = self._optimize_budget_allocation(itinerary, budget)

        return itinerary

    def _build_itinerary_prompt(self, context: Dict[str, Any]) -> str:
        """Build detailed prompt for AI"""
        return f"""
        As a travel planning expert, create a detailed {context['duration_days']}-day itinerary for {context['destination']}.

        Constraints:
        - Total budget: ${context['total_budget']} (${context['budget_per_day']:.2f} per day)
        - Travel style: {', '.join(context['preferences'].get('travel_style', []))}
        - Preferred activities: {', '.join(context['preferences'].get('activities', []))}
        - Season: {context['current_season']}

        Requirements:
        1. Break down each day into morning, afternoon, evening
        2. Include estimated costs for each activity
        3. Include transportation between locations
        4. Factor in meal costs
        5. Consider opening hours and travel time
        6. Include free/cheap alternatives for budget flexibility

        Format as JSON with:
        - daily_itinerary: array of days
        - budget_breakdown: accommodation, food, activities, transportation
        - money_saving_tips: array of tips
        - recommended_bookings: flights, hotels if dates provided
        """

    def _optimize_budget_allocation(
            self,
            itinerary: Dict[str, Any],
            total_budget: float
    ) -> Dict[str, Any]:
        """Optimize budget distribution"""
        # Implement budget optimization logic
        # This could use linear programming or rule-based allocation

        categories = ["accommodation", "food", "activities", "transportation", "misc"]

        # Simple rule-based allocation for now
        allocation_rules = {
            "accommodation": 0.35,  # 35% for lodging
            "food": 0.25,  # 25% for meals
            "activities": 0.20,  # 20% for activities
            "transportation": 0.15,  # 15% for transport
            "misc": 0.05  # 5% miscellaneous
        }

        optimized_budget = {}
        for category, percentage in allocation_rules.items():
            optimized_budget[category] = {
                "allocated": total_budget * percentage,
                "suggested_min": total_budget * (percentage - 0.05),
                "suggested_max": total_budget * (percentage + 0.05)
            }

        itinerary["optimized_budget"] = optimized_budget
        return itinerary

    def _get_season(self, date: datetime) -> str:
        """Determine season from date"""
        month = date.month
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        else:
            return "fall"