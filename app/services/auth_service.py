# app/services/auth_service.py
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.token import Token
from app.utils.auth import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    decode_token, validate_email, validate_password
)
from app.core.config import settings


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, email: str, username: str, password: str,
                      full_name: Optional[str] = None) -> Dict[str, Any]:
        """Register a new user"""
        # Validate email
        if not validate_email(email):
            return {
                "success": False,
                "error": "Invalid email format"
            }

        # Validate password
        password_validation = validate_password(password)
        if not password_validation["is_valid"]:
            return {
                "success": False,
                "error": "Password validation failed",
                "details": password_validation["errors"]
            }

        # Check if user exists
        existing_user = self.db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()

        if existing_user:
            return {
                "success": False,
                "error": "Email or username already registered"
            }

        # Create new user
        hashed_password = hash_password(password)
        user = User(
            email=email,
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            is_verified=False,  # Email verification would be added here
            preferences={
                "language": "en",
                "timezone": "UTC",
                "currency": "USD"
            }
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return {
            "success": True,
            "user_id": user.id,
            "message": "User registered successfully"
        }

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user = self.db.query(User).filter(User.email == email).first()

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        self.db.commit()

        return user

    def create_user_tokens(self, user: User) -> Dict[str, str]:
        """Create access and refresh tokens for user"""
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "username": user.username
        }

        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        # Store refresh token in database
        token = Token(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )

        self.db.add(token)
        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, str]]:
        """Refresh access token using refresh token"""
        # Verify refresh token exists in database
        token = self.db.query(Token).filter(
            Token.refresh_token == refresh_token,
            Token.expires_at > datetime.utcnow()
        ).first()

        if not token:
            return None

        # Decode token
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        # Create new access token
        token_data = {
            "sub": payload.get("sub"),
            "user_id": payload.get("user_id"),
            "username": payload.get("username")
        }

        new_access_token = create_access_token(token_data)

        # Update token in database
        token.access_token = new_access_token
        self.db.commit()

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    def get_current_user(self, token: str) -> Optional[User]:
        """Get user from token"""
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return None

        user_id = payload.get("user_id")
        if not user_id:
            return None

        # Verify token exists in database (optional, for token revocation)
        db_token = self.db.query(Token).filter(
            Token.access_token == token,
            Token.expires_at > datetime.utcnow()
        ).first()

        if not db_token:
            return None

        # Get user
        user = self.db.query(User).filter(User.id == user_id).first()
        return user if user and user.is_active else None

    def logout_user(self, token: str) -> bool:
        """Logout user by removing token"""
        db_token = self.db.query(Token).filter(Token.access_token == token).first()
        if db_token:
            self.db.delete(db_token)
            self.db.commit()
            return True
        return False

    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "is_verified": user.is_verified,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login": user.last_login.isoformat() if user.last_login else None,
            "preferences": user.preferences
        }

    def update_user_profile(self, user_id: int, updates: Dict[str, Any]) -> bool:
        """Update user profile"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Allowed fields to update
        allowed_fields = ["full_name", "preferences"]

        for field, value in updates.items():
            if field in allowed_fields and hasattr(user, field):
                setattr(user, field, value)

        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        return True

    def change_password(self, user_id: int, old_password: str, new_password: str) -> Dict[str, Any]:
        """Change user password"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "error": "User not found"}

        # Verify old password
        if not verify_password(old_password, user.hashed_password):
            return {"success": False, "error": "Incorrect old password"}

        # Validate new password
        password_validation = validate_password(new_password)
        if not password_validation["is_valid"]:
            return {
                "success": False,
                "error": "New password validation failed",
                "details": password_validation["errors"]
            }

        # Update password
        user.hashed_password = hash_password(new_password)
        self.db.commit()

        return {"success": True, "message": "Password changed successfully"}