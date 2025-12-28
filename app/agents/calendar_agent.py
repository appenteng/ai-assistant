"""
Calendar and scheduling agent
"""
from app.agents.base_agent import BaseAgent
from app.services.calendar_service import CalendarService
from datetime import datetime
from typing import Dict, List

class CalendarAgent(BaseAgent):
    def __init__(self, user_id: int = None):
        super().__init__(user_id)
        self.calendar = CalendarService()
    
    async def execute(self, task: Dict) -> Dict:
        """Handle calendar-related tasks"""
        action = task.get('action')
        
        if action == "schedule_meeting":
            return await self.schedule_meeting(task)
        elif action == "find_free_time":
            return await self.find_free_time(task)
        elif action == "reschedule_conflicts":
            return await self.reschedule_conflicts()
        else:
            return {"error": f"Unknown action: {action}"}
    
    async def schedule_meeting(self, task: Dict) -> Dict:
        """Schedule a meeting based on preferences"""
        participants = task.get('participants', [])
        duration = task.get('duration', 60)
        topic = task.get('topic', 'Meeting')
        
        # Find optimal time
        optimal_time = await self._find_optimal_time(participants, duration)
        
        # Create event
        event = await self.calendar.create_event(
            title=topic,
            start_time=optimal_time,
            duration=duration,
            participants=participants
        )
        
        # Send invites
        await self.calendar.send_invites(event, participants)
        
        return {
            "status": "scheduled",
            "event": event,
            "time": optimal_time.isoformat()
        }