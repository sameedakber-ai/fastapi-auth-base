from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from app.core.config import settings
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.schemas.token import TokenPayload
from app.schemas.user import User as UserSchema
from app.db.models import User as DBUser

from app.db.session import get_db

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

oauth2_scheme = HTTPBearer()

async def get_current_user(
    bearer: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> UserSchema:
    token = bearer.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        token_data = TokenPayload(**payload)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not token_data.sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    user = db.query(DBUser).filter(DBUser.id == int(token_data.sub)).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user")

    return user

    