"""
TalentSpark AI — JWT Token Utilities
Access token and refresh token creation/verification.
"""

from fastapi import HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "talentspark_default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token with user data."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    """Create a longer-lived JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str) -> dict:
    """Verify and decode a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid credentials: no user ID in token")
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


def verify_refresh_token(token: str) -> dict:
    """Verify and decode a JWT refresh token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


def create_reset_token(email: str) -> str:
    """Create a short-lived token for password reset."""
    expire = datetime.utcnow() + timedelta(hours=1)
    return jwt.encode({"sub": email, "exp": expire, "type": "reset"}, SECRET_KEY, algorithm=ALGORITHM)


def verify_reset_token(token: str) -> str:
    """Verify a password reset token, returns the email."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None or payload.get("type") != "reset":
            raise HTTPException(status_code=400, detail="Invalid reset token")
        return email
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
