from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.user import User as UserSchema, UserCreate
from app.db.models import User as DBUser
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_password_hash
from app.core.deps import get_current_active_admin, get_current_active_hr, get_current_active_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post('/', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    pwd_hash = get_password_hash(user.password)
    new_user_data = {
        "email": user.email,
        "hashed_password": pwd_hash
    }
    new_user = DBUser(**new_user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/', response_model=list[UserSchema])
async def read_users(db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_active_hr)):
    db_users = db.query(DBUser).all()
    return db_users

@router.get('/{user_id}', response_model=UserSchema)
async def read_user(user_id: int, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_active_hr)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    # if current_user.id != user_id and current_user.role not in ['admin', 'hr']:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user