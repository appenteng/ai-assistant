# simple_main.py - TEMPORARY to get dashboard working
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

app = FastAPI(title="AI Assistant", version="1.0.0")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Simple endpoints for dashboard
@app.get("/")
async def dashboard(request: Request):
    """Serve the main dashboard"""
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AI Assistant"}


# Mock API endpoints for the dashboard
@app.get("/api/travel/plan-simple")
async def mock_plan_trip(destination: str = "Paris", days: int = 3, budget: float = 1000):
    """Mock trip planning for dashboard testing"""
    return {
        "status": "success",
        "plan": {
            "destination": destination,
            "days": days,
            "itinerary": [
                f"Day 1: Arrive in {destination}, check in, explore city center",
                f"Day 2: Visit major attractions in {destination}",
                f"Day 3: Last-minute shopping, depart from {destination}"
            ],
            "total_cost": days * 150,
            "within_budget": (days * 150) <= budget,
            "cost_breakdown": {
                "accommodation": days * 60,
                "food": days * 40,
                "activities": days * 30,
                "transportation": days * 20
            }
        }
    }


@app.get("/api/chat")
async def mock_chat(message: str = "Hello"):
    """Mock chat for dashboard testing"""
    responses = {
        "hello": "Hi there! I'm your AI Assistant. How can I help?",
        "travel": "I can help plan trips! Try the travel planning feature.",
        "help": "I can assist with trip planning, answer questions, and more!"
    }

    msg_lower = message.lower()
    for key, response in responses.items():
        if key in msg_lower:
            return {"response": response}

    return {"response": f"I received: '{message}'. How can I assist you?"}


if __name__ == "__main__":
    print("🚀 SIMPLE AI Assistant starting...")
    print("🌐 Dashboard: http://localhost:8000")
    print("💬 Mock chat interface available!")
    print("✈️  Mock trip planner ready!")
    print("\n⚠️  NOTE: This is a simplified version for testing UI.")
    print("   To use full features, fix the config errors.")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)