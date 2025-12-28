# backend/app/services/admin_service.py
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import psutil
import os
from app.models.user import User
from app.models.trip import Trip


class AdminService:
    @staticmethod
    def get_users(
            db: Session,
            page: int = 1,
            limit: int = 20,
            search: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get paginated user list"""
        query = db.query(User)

        if search:
            query = query.filter(
                (User.email.ilike(f"%{search}%")) |
                (User.full_name.ilike(f"%{search}%"))
            )

        total = query.count()
        offset = (page - 1) * limit

        users = query.order_by(desc(User.created_at)) \
            .offset(offset) \
            .limit(limit) \
            .all()

        return {
            "users": users,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (total + limit - 1) // limit
            }
        }

    @staticmethod
    def get_user_statistics(db: Session, period: str) -> Dict[str, Any]:
        """Get user statistics for given period"""
        now = datetime.now()

        if period == "24h":
            start_date = now - timedelta(days=1)
        elif period == "7d":
            start_date = now - timedelta(days=7)
        elif period == "30d":
            start_date = now - timedelta(days=30)
        elif period == "90d":
            start_date = now - timedelta(days=90)
        else:  # 1y
            start_date = now - timedelta(days=365)

        # New users in period
        new_users = db.query(User).filter(
            User.created_at >= start_date
        ).count()

        # Active users (users with trips)
        active_users = db.query(func.count(func.distinct(Trip.user_id))).filter(
            Trip.created_at >= start_date
        ).scalar()

        # Total trips created
        total_trips = db.query(func.count(Trip.id)).filter(
            Trip.created_at >= start_date
        ).scalar()

        return {
            "period": period,
            "new_users": new_users,
            "active_users": active_users,
            "total_trips": total_trips,
            "avg_trips_per_user": total_trips / active_users if active_users > 0 else 0
        }

    @staticmethod
    def get_system_metrics() -> Dict[str, Any]:
        """Get system performance metrics"""
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memory usage
        memory = psutil.virtual_memory()

        # Disk usage
        disk = psutil.disk_usage('/')

        # Process info
        process = psutil.Process(os.getpid())

        return {
            "cpu_percent": cpu_percent,
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            },
            "process": {
                "memory_mb": process.memory_info().rss / 1024 / 1024,
                "cpu_percent": process.cpu_percent(),
                "threads": process.num_threads()
            },
            "timestamp": datetime.now().isoformat()
        }