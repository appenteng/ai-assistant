# backend/app/services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional
from app.core.config import settings
import jwt
from datetime import datetime, timedelta


class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.base_url = settings.BASE_URL

    def send_verification_email(self, email: str, token: str) -> bool:
        """Send email verification link"""
        verification_url = f"{self.base_url}/verify-email?token={token}"

        html = f"""
        <html>
            <body>
                <h2>Verify Your Email</h2>
                <p>Click the link below to verify your email address:</p>
                <a href="{verification_url}">Verify Email</a>
                <p>This link will expire in 24 hours.</p>
            </body>
        </html>
        """

        return self._send_email(
            to_email=email,
            subject="Verify Your Email",
            html_content=html
        )

    def send_password_reset_email(self, email: str, token: str) -> bool:
        """Send password reset email"""
        reset_url = f"{self.base_url}/reset-password?token={token}"

        html = f"""
        <html>
            <body>
                <h2>Reset Your Password</h2>
                <p>Click the link below to reset your password:</p>
                <a href="{reset_url}">Reset Password</a>
                <p>This link will expire in 1 hour.</p>
                <p>If you didn't request this, please ignore this email.</p>
            </body>
        </html>
        """

        return self._send_email(
            to_email=email,
            subject="Reset Your Password",
            html_content=html
        )