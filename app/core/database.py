# app/core/database.py - PRODUCTION READY
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def init_db():
    """Initialize database tables"""
    print("📦 Initializing database...")

    # Import all models here so they're registered with Base
    from app.models.user import User
    from app.models.token import Token
    from app.models.trip import Trip  # If you have this

    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_session():
    """Get database session directly"""
    return SessionLocal()