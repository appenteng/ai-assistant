"""
Base class for all AI agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from app.services.openai_service import OpenAIService
from app.services.memory_service import MemoryService

class BaseAgent(ABC):
    def __init__(self, user_id: int = None):
        self.user_id = user_id
        self.ai = OpenAIService()
        self.memory = MemoryService(user_id)
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main task"""
        pass
    
    async def plan(self, goal: str) -> List[str]:
        """Break down goal into steps"""
        prompt = f"Break this goal into steps: {goal}"
        response = await self.ai.chat(prompt)
        return self._parse_steps(response)
    
    def _parse_steps(self, response: str) -> List[str]:
        # Parse LLM response into steps
        return [step.strip() for step in response.split("\n") if step.strip()]