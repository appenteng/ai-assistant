"""
Task schemas
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class TaskBase(BaseModel):
    task_type: str
    description: str
    input_data: Optional[Dict[str, Any]] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    status: str
    progress: int
    result_data: Optional[Dict[str, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None