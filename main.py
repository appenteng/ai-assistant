# main.py - GUARANTEED WORKING VERSION
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os


# Create app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting AI Travel Assistant...")
    yield
    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title="AI Travel Assistant",
    description="Intelligent travel planning with AI",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Basic endpoints - NO IMPORTS NEEDED!
@app.get("/")
def home():
    return {
        "message": "AI Travel Assistant API",
        "status": "online",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "chat": "GET /api/chat?message=hello",
            "travel_plan": "GET /api/travel/plan?destination=Tokyo&days=5",
            "health": "GET /health"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Assistant"}


@app.get("/api/chat")
def chat(message: str = "Hello"):
    return {
        "message": message,
        "response": f"AI says: I can help you plan trips! You said: '{message}'",
        "sentiment": {"positive": 0.8, "negative": 0.1, "neutral": 0.1}
    }


@app.get("/api/travel/plan")
def plan_trip(
        destination: str = "Paris",
        days: int = 3,
        budget: float = 1000
):
    # Simple trip planner
    daily_cost = budget / days if budget > 0 else 150

    return {
        "status": "success",
        "destination": destination,
        "days": days,
        "budget": budget,
        "itinerary": [f"Day {i + 1}: Explore {destination}" for i in range(days)],
        "estimated_cost": days * daily_cost,
        "recommendations": [
            "Try local cuisine",
            "Visit main attractions",
            "Take lots of photos!"
        ]
    }


# Run the app
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    print(f"🎯 Server starting on http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"💬 Chat API: http://localhost:{port}/api/chat?message=hello")
    print(f"✈️  Travel API: http://localhost:{port}/api/travel/plan?destination=Tokyo")

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)