# main.py - PRODUCTION READY
from fastapi import FastAPI
from app.api.router import api_router
import uvicorn
import os

app = FastAPI(
    title="AI Travel Assistant",
    description="Intelligent travel planning and task automation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include API routes
app.include_router(api_router, prefix="/api")

@app.get("/")
def home():
    return {
        "message": "AI Travel Assistant API",
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "chat": "/api/chat",
            "travel_plan": "/api/travel/plan",
            "destinations": "/api/travel/destinations"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Assistant"}

# For local development
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)