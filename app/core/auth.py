from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from app.core.config import settings
from typing import Optional

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates an access token string by encoding the payload
    """
    payload = data.copy()
    if expires_delta:
        token_expire_date = datetime.now(timezone.utc) + expires_delta
    else:
        token_expire_date = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload['exp'] = token_expire_date
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a refresh token string by encoding the payload
    """
    payload = data.copy()
    if expires_delta:
        token_expire_date = datetime.now(timezone.utc) + expires_delta
    else:
        token_expire_date = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    
    payload['exp'] = token_expire_date
    return jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
    