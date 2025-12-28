"""
Memory/Context storage for AI
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func
from app.core.database import Base

class UserMemory(Base):
    __tablename__ = "user_memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    
    # Memory content
    memory_type = Column(String)  # "preference", "fact", "pattern"
    key = Column(String)  # e.g., "favorite_airline"
    value = Column(JSON)  # e.g., {"airline": "Delta", "reason": "comfort"}
    
    # Context
    context = Column(Text)  # How/why this memory was created
    source = Column(String)  # "user_input", "inferred", "system"
    confidence = Column(Integer)  # 0-100
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_accessed = Column(DateTime(timezone=True), onupdate=func.now())