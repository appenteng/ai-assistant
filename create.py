#!/usr/bin/env python3
"""
AI Assistant Project Generator
Run this script to create the complete project structure with all files
"""

import os
import sys
from pathlib import Path

def create_file(path, content):
    """Create a file with content"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ Created: {path}")

def main():
    project_name = "ai_assistant"

    print(f"🚀 Creating {project_name} project structure...")

    # Create root directory
    os.makedirs(project_name, exist_ok=True)

    # 1. ROOT LEVEL FILES
    root_files = {
        "main.py": """from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.router import router
from app.core.config import settings
from app.core.database import init_db
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    \"\"\"Startup and shutdown events\"\"\"
    # Startup
    await init_db()
    print("🚀 AI Assistant starting up...")
    yield
    # Shutdown
    print("👋 Shutting down...")

app = FastAPI(
    title="Personal AI Assistant",
    version="1.0.0",
    lifespan=lifespan
)

# Include all routers
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "AI Assistant API", "status": "online"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)""",
        "requirements.txt": """# Core
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# AI/ML
openai==1.3.0
langchain==0.0.340
langchain-openai==0.0.2
tiktoken==0.5.1

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1

# Data
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0

# APIs
requests==2.31.0
aiohttp==3.9.1
httpx==0.25.1

# Background jobs
celery==5.3.4

# Utilities
loguru==0.7.2
pytest==7.4.3
pytest-asyncio==0.21.1""",        ".env": """# Database
DATABASE_URL=postgresql://user:password@localhost/ai_assistant_dev
REDIS_URL=redis://localhost:6379/0

# AI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview

# External APIs (optional for start)
GOOGLE_API_KEY=
SKYSCANNER_API_KEY=
BOOKING_COM_API_KEY=

# Security
SECRET_KEY=your-super-secret-key-change-this""",

        ".gitignore": """# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.venv/
.env

# Virtual Environment
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite3

# Coverage
.coverage
htmlcov/

# Distribution
dist/
build/
*.egg-info/""",