from fastapi import APIRouter, HTTPException, status, Depends
from app.db.session import get_db
from app.schemas.token import Token, TokenPayload
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.models import User as DBUser
from app.core.security import verify_password
from app.core.auth import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.email == form_data.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or passowrd", headers={"WWW-Authenticate": "Bearer"})
    data = {
        "sub": db_user.id,
        "email": db_user.email
    }
    token = create_access_token(data)
    return Token(
        access_token=token,
        token_type="bearer"
    )
