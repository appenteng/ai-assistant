"""
Travel planning agent
"""
from app.agents.base_agent import BaseAgent
from app.services.travel_service import TravelService
from typing import Dict, Any, List

class TravelAgent(BaseAgent):
    def __init__(self, user_id: int = None):
        super().__init__(user_id)
        self.travel_service = TravelService()
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute travel planning task"""
        try:
            # Step 1: Understand request
            requirements = await self._understand_request(task)
            
            # Step 2: Check memory for preferences
            preferences = await self.memory.get_travel_preferences()
            
            # Step 3: Plan itinerary
            itinerary = await self._plan_itinerary(requirements, preferences)
            
            # Step 4: Book components
            bookings = await self._book_components(itinerary)
            
            # Step 5: Save to memory
            await self._save_travel_memory(itinerary)
            
            return {
                "status": "success",
                "itinerary": itinerary,
                "bookings": bookings,
                "summary": f"Trip to {task.get('destination')} planned successfully"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _understand_request(self, task: Dict) -> Dict:
        prompt = f"""
        Extract travel requirements from: {task}
        
        Return JSON with:
        - destination
        - budget
        - dates (start/end)
        - travelers (count, ages)
        - preferences (activities, pace)
        - constraints
        """
        return await self.ai.structured_response(prompt)
    
    async def _plan_itinerary(self, requirements: Dict, preferences: Dict) -> Dict:
        # Use AI to create detailed itinerary
        prompt = f"""
        Create detailed itinerary with:
        Requirements: {requirements}
        User preferences: {preferences}
        
        Include:
        1. Daily schedule
        2. Accommodation options
        3. Transportation
        4. Activities
        5. Estimated costs
        """
        return await self.ai.structured_response(prompt)
    
    async def _book_components(self, itinerary: Dict) -> List[Dict]:
        bookings = []
        
        # Book flights
        if itinerary.get('flights'):
            flights = await self.travel_service.search_flights(
                origin=itinerary['origin'],
                destination=itinerary['destination'],
                dates=itinerary['dates']
            )
            bookings.append({"type": "flight", "data": flights})
        
        # Book hotels
        if itinerary.get('accommodation'):
            hotels = await self.travel_service.search_hotels(
                location=itinerary['destination'],
                dates=itinerary['dates']
            )
            bookings.append({"type": "hotel", "data": hotels})
        
        return bookings
    
    async def _save_travel_memory(self, itinerary: Dict):
        await self.memory.store({
            "type": "travel_pattern",
            "data": {
                "destination": itinerary.get('destination'),
                "preferred_activities": itinerary.get('activities'),
                "average_budget": itinerary.get('estimated_cost')
            }
        })