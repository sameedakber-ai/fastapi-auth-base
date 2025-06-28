from fastapi import Depends, HTTPException, status
from app.schemas.user import User as UserSchema
from app.core.auth import get_current_user

def get_current_active_user(current_user: UserSchema = Depends(get_current_user)) -> UserSchema:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def get_current_active_admin(current_user: UserSchema = Depends(get_current_user)) -> UserSchema:
    if current_user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

def get_current_active_hr(current_user: UserSchema = Depends(get_current_user)) -> UserSchema:
    if current_user.role not in ['hr', 'admin']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return current_user

