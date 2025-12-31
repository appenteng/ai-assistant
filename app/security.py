# app/utils/security.py

from datetime import datetime, timedelta
from typing import Optional
import hashlib
import secrets

# Simple password hashing for now (replace with bcrypt in production)
def get_password_hash(password: str) -> str:
    """Simple password hash for testing - REPLACE with proper bcrypt in production"""
    salt = secrets.token_hex(8)
    return f"{salt}${hashlib.sha256((salt + password).encode()).hexdigest()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Simple password verification - REPLACE with proper bcrypt in production"""
    if "$" not in hashed_password:
        return False
    salt, hash_value = hashed_password.split("$", 1)
    test_hash = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return test_hash == hash_value

# Simple JWT token functions
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create simple access token for testing"""
    import json
    import base64

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)

    data["exp"] = expire.isoformat()

    # Simple base64 encoding for testing
    token = base64.b64encode(json.dumps(data).encode()).decode()
    return token

def verify_token(token: str):
    """Verify simple token"""
    try:
        import json
        import base64

        data = json.loads(base64.b64decode(token).decode())

        # Check expiration
        if "exp" in data:
            expire = datetime.fromisoformat(data["exp"])
            if datetime.utcnow() > expire:
                return None

        return data.get("sub")
    except:
        return None