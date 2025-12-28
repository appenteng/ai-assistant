# hybrid_app.py - Combines working test with your structure
from fastapi import FastAPI, APIRouter
import uvicorn

# Create routers like in your structure
main_router = APIRouter()
travel_router = APIRouter()

# Simple services
class AIService:
    def chat(self, message):
        return f"AI: I heard '{message}'"

class TravelService:
    def plan_trip(self, destination, days):
        return {
            "destination": destination,
            "days": days,
            "itinerary": [f"Day {i+1}: Explore {destination}" for i in range(days)]
        }

ai_service = AIService()
travel_service = TravelService()

# Routes from your main.py
@main_router.get("/test")
def test_endpoint():
    return {"message": "API is working!"}

@main_router.post("/chat")
def chat_with_ai(message: str):
    response = ai_service.chat(message)
    return {"ai_response": response}

# Routes from your travel.py
@travel_router.get("/plan")
def plan_trip(destination: str = "Paris", days: int = 3):
    plan = travel_service.plan_trip(destination, days)
    return plan

# Combine routers like your router.py
api_router = APIRouter()
api_router.include_router(main_router, tags=["main"])
api_router.include_router(travel_router, prefix="/travel", tags=["travel"])

# Main app like your main.py
app = FastAPI(title="AI Assistant")
app.include_router(api_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "AI Assistant API", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    print("🚀 Hybrid App Starting...")
    print("🌐 Open: http://localhost:8000")
    print("🔗 Test: http://localhost:8000/api/travel/plan?destination=Tokyo")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)