# --- MODULE IMPORTS ---
from fastapi import APIRouter, FastAPI
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User as DBUser
from app.core.security import get_password_hash
from app.schemas.user import UserCreate
from app.schemas.user import User as UserSchema

# Initialize FastAPI application
app = FastAPI(
    title="Job Portal API",
    description="Backend API for the Learnobots Job Portal, managing jobs, applications, and user data.",
    version="0.1.0",
    docs_url="/docs", # for swagger UI at /docs
    redoc_url="/redoc" # for ReDoc UI at /redoc
)

# Define a simple root endpoint
@app.get('/')
async def read_root():
    """
    Root endpoint to check if the API is running.
    Returns a simple welcome message
    """
    return {"message": "Welcome to the Learnobots Job Portal API!"}

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
async def read_users(db: Session = Depends(get_db)):
    db_users = db.query(DBUser).all()
    return db_users

@router.get('/{user_id}', response_model=UserSchema)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

app.include_router(router)