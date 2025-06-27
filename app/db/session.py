from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# --- CREATE SQLALCHEMY ENGINE ---
engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True, echo=False)

# --- CONFIGURE SESSIONMAKER FOR NEW DATABASE SESSIONS ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- BASE CLASS FOR DATABASE TABLES ---
Base = declarative_base()

# --- GET DATABASE SESSION FOR FASTAPI ENDPOINTS ---
def get_db():
    """
    Dependency function that yields a SQLAlchemy database session.
    This session is automatically closed after the request is processed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()