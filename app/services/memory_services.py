"""
Memory storage and retrieval
"""
from typing import Dict, List, Any, Optional
import json
from datetime import datetime
from app.core.database import SessionLocal
from app.models.memory import UserMemory

class MemoryService:
    def __init__(self, user_id: int):
        self.user_id = user_id
    
    async def store(self, memory: Dict) -> None:
        """Store a memory"""
        db = SessionLocal()
        try:
            memory_record = UserMemory(
                user_id=self.user_id,
                memory_type=memory.get('type'),
                key=memory.get('key'),
                value=json.dumps(memory.get('value')),
                context=memory.get('context'),
                source=memory.get('source', 'system'),
                confidence=memory.get('confidence', 80)
            )
            db.add(memory_record)
            db.commit()
        finally:
            db.close()
    
    async def retrieve(self, query: str, limit: int = 5) -> List[Dict]:
        """Retrieve relevant memories"""
        # In production, use vector search
        # For now, simple keyword search
        db = SessionLocal()
        try:
            memories = db.query(UserMemory).filter(
                UserMemory.user_id == self.user_id
            ).order_by(
                UserMemory.last_accessed.desc()
            ).limit(limit).all()
            
            return [
                {
                    "key": m.key,
                    "value": json.loads(m.value),
                    "confidence": m.confidence
                }
                for m in memories
            ]
        finally:
            db.close()
    
    async def get_travel_preferences(self) -> Dict:
        """Get user's travel preferences from memory"""
        memories = await self.retrieve("travel")
        
        preferences = {
            "preferred_airlines": [],
            "seat_preference": "aisle",
            "hotel_standard": "4_star",
            "activities": [],
            "dietary_restrictions": []
        }
        
        # Merge memories into preferences
        for memory in memories:
            if "airline" in memory.get('value', {}):
                preferences["preferred_airlines"].append(memory['value']['airline'])
        
        return preferences