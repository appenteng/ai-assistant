class TravelAgent:
    def __init__(self):
        self.openai_service = OpenAIService()
        self.travel_service = TravelService()
    
    async def plan(self, destination, budget, dates):
        # Step 1: Use AI to understand request
        plan = await self.openai_service.create_itinerary(
            destination, budget, dates
        )
        
        # Step 2: Book actual components
        bookings = await self.travel_service.book_flights(plan)
        
        return {
            "itinerary": plan,
            "bookings": bookings,
            "status": "planned"
        }