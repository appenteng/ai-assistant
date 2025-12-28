"""
Task management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import TaskService
from app.core.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user)
):
    """Create a new task"""
    service = TaskService(current_user.id)
    
    # Start task in background
    task_id = await service.create_task(task)
    
    # Queue for processing
    background_tasks.add_task(
        service.process_task,
        task_id=task_id
    )
    
    return {"task_id": task_id, "status": "queued"}

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user = Depends(get_current_user)
):
    """Get task status and result"""
    service = TaskService(current_user.id)
    task = await service.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return task