# --- MODULE IMPORTS ---
from fastapi import FastAPI

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

