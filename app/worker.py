"""
Celery worker for background tasks
"""
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "ai_assistant",
    broker=settings.redis_url,
    backend=settings.redis_url
)

@celery_app.task
def process_task_async(task_id: int):
    """Process task in background"""
    from app.services.task_service import TaskService
    service = TaskService()
    service.process_task(task_id)