# main.py - UPDATED VERSION THAT SERVES FRONTEND TOO

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
import threading
import webbrowser
import time

app = FastAPI(title="AI Travel Assistant")

# Mount frontend folder
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")


# Serve frontend at root
@app.get("/")
async def serve_frontend():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not found. Please create frontend/index.html"}


# Your existing API endpoints
@app.get("/api/chat")
def chat(message: str = "Hello"):
    return {
        "message": message,
        "response": f"AI says: I can help you plan trips! You said: '{message}'",
        "sentiment": {"positive": 0.8, "negative": 0.1, "neutral": 0.1}
    }


@app.get("/api/travel/plan")
def plan_trip(destination: str = "Paris", days: int = 3, budget: float = 1000):
    return {
        "status": "success",
        "destination": destination,
        "days": days,
        "budget": budget,
        "itinerary": [f"Day {i + 1}: Explore {destination}" for i in range(days)],
        "estimated_cost": days * 150,
        "recommendations": ["Try local cuisine", "Visit attractions", "Enjoy!"]
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Assistant"}


# Function to open browser automatically
def open_browser():
    time.sleep(2)  # Wait for server to start
    webbrowser.open("http://localhost:8080")


if __name__ == "__main__":
    port = 8080

    # Start browser in background thread
    threading.Thread(target=open_browser, daemon=True).start()

    print("🚀 Starting AI Travel Assistant...")
    print(f"🌐 Frontend: http://localhost:{port}")
    print(f"🔧 Backend API: http://localhost:{port}/api/chat")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print("----------------------------------------")

    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)