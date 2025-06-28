# --- MODULE IMPORTS ---
from fastapi import APIRouter, FastAPI
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User as DBUser
from app.core.security import get_password_hash
from app.schemas.user import UserCreate
from app.schemas.user import User as UserSchema
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password
from app.schemas.token import Token
from app.core.config import settings

from app.api.auth import router as auth_router
from app.api.users import router as user_router

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

app.include_router(auth_router)
app.include_router(user_router)