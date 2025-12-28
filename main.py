# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.router import api_router
from app.core.database import init_db
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting AI Assistant...")
    init_db()  # Initialize database tables
    print("✅ Database initialized")
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

# Include API router
app.include_router(api_router, prefix="/api")

@app.get("/")
def home():
    return {
        "message": "AI Travel Assistant API",
        "status": "online",
        "version": "1.0.0",
        "database": "connected",
        "docs": "/docs",
        "endpoints": {
            "chat": "GET /api/chat?message=hello",
            "travel_plan": "GET /api/travel/plan?destination=Tokyo&days=5",
            "destinations": "GET /api/travel/destinations"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Assistant",
        "database": "connected"
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🌐 Server starting on http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)


# In main.py - Make sure this exists
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add at the top
import os
from fastapi.middleware.cors import CORSMiddleware

# Update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "https://your-frontend-domain.vercel.app",  # Will update after deployment
        "*"  # For testing, remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add production check
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info"
    )