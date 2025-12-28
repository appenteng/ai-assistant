# backend/app/api/admin.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.api.deps import get_current_user, get_db, require_admin
from app.models.user import User
from app.schemas.admin import (
    UserStats, SystemMetrics, AnalyticsResponse
)
from app.services.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", dependencies=[Depends(require_admin)])
async def get_users(
        page: int = Query(1, ge=1),
        limit: int = Query(20, ge=1, le=100),
        search: Optional[str] = None,
        db: Session = Depends(get_db)
):
    """Admin: Get all users with pagination"""
    return AdminService.get_users(db, page, limit, search)


@router.get("/stats", response_model=UserStats, dependencies=[Depends(require_admin)])
async def get_user_stats(
        period: str = Query("7d", regex="^(24h|7d|30d|90d|1y)$"),
        db: Session = Depends(get_db)
):
    """Admin: Get user statistics"""
    return AdminService.get_user_statistics(db, period)


@router.get("/analytics", response_model=AnalyticsResponse, dependencies=[Depends(require_admin)])
async def get_analytics(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        db: Session = Depends(get_db)
):
    """Admin: Get system analytics"""
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    return AdminService.get_analytics(db, start_date, end_date)


@router.get("/system-metrics", response_model=SystemMetrics, dependencies=[Depends(require_admin)])
async def get_system_metrics():
    """Admin: Get system performance metrics"""
    return AdminService.get_system_metrics()