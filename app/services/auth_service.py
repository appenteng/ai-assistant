from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.auth import UserCreate
from fastapi import HTTPException, status

# SIMPLE PASSWORD FUNCTIONS (temporary - replace with proper security)
def get_password_hash(password: str) -> str:
    """Simple password hash for testing - REPLACE with proper bcrypt in production"""
    import hashlib
    import secrets
    salt = secrets.token_hex(8)
    return f"{salt}${hashlib.sha256((salt + password).encode()).hexdigest()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Simple password verification - REPLACE with proper bcrypt in production"""
    if "$" not in hashed_password:
        return False
    salt, hash_value = hashed_password.split("$", 1)
    import hashlib
    test_hash = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return test_hash == hash_value


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: UserCreate) -> User:
        """Register a new user"""
        # Check if user exists
        existing_user = self.db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()

        if existing_user:
            if existing_user.email == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already taken"
                )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user credentials"""
        user = self.db.query(User).filter(
            (User.email == username) | (User.username == username)
        ).first()

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()