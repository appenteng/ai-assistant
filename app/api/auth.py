# backend/app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserResponse, Token, TokenRefresh
from app.services.user_service import UserService
from app.core.security import SecurityService
from app.services.email_service import EmailService

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
        user_data: UserCreate,
        db: Session = Depends(get_db)
):
    """Register new user and send verification email"""
    user = UserService.create_user(db, user_data)

    # Create verification token
    verification_token = SecurityService.create_access_token(
        {"sub": str(user.id), "email": user.email},
        expires_delta=timedelta(hours=24)
    )

    # Send verification email
    email_service = EmailService()
    email_service.send_verification_email(user.email, verification_token)

    return user


@router.post("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify user's email"""
    payload = SecurityService.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    user = UserService.verify_user_email(db, payload.get("email"))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"message": "Email verified successfully"}


@router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """Login user and return access/refresh tokens"""
    user = UserService.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Create tokens
    access_token = SecurityService.create_access_token(
        {"sub": str(user.id), "email": user.email}
    )
    refresh_token = SecurityService.create_refresh_token(
        {"sub": str(user.id), "email": user.email}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh):
    """Refresh access token"""
    tokens = SecurityService.refresh_access_token(token_data.refresh_token)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    return {
        "access_token": tokens[0],
        "refresh_token": tokens[1],
        "token_type": "bearer"
    }


@router.post("/forgot-password")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    """Request password reset"""
    user = UserService.get_user_by_email(db, email)
    if user:
        # Create reset token
        reset_token = SecurityService.create_access_token(
            {"sub": str(user.id), "email": user.email},
            expires_delta=timedelta(hours=1)
        )

        # Send reset email
        email_service = EmailService()
        email_service.send_password_reset_email(user.email, reset_token)

    # Always return success to prevent email enumeration
    return {"message": "If email exists, reset instructions sent"}