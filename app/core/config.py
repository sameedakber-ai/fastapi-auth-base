# --- MODULE IMPORTS ---
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )
    DATABASE_URL: PostgresDsn = Field(
        ...,
        env="DATABASE_URL",
        description="The postgreSQL database connection URL (e.g., postgresql://user:password@host:port/dbname)"
    )
    PROJECT_NAME: str = Field(
        default="Learnobots Job Portal API",
        env="PROJECT_NAME",
        description="Name of the FastAPI project"
    )
    API_V1_STR: str = Field(
        default="/api/v1",
        env="API_V1_STR",
        description="Base path for API version 1 endpoints."
    )
    SECRET_KEY: str = Field(
        ...,
        env="SECRET_KEY",
        description="Secret key used to sign JWTs"
    )
    ALGORITHM: str = Field(
        default="HS256",
        env="ALGORITHM",
        description="The hashing algorithm for JWTs."
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        env="ACCESS_TOKEN_EXPIRE_MINUTES",
        description="The lifespan of access tokens in minutes."
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        env="REFRESH_TOKEN_EXPIRE_DAYS",
        description="The lifespan of refresh tokens in days"
    )

settings = Settings()
print(f"Loading settings for: {settings.PROJECT_NAME}")
print(f"API Base Path: {settings.API_V1_STR}")