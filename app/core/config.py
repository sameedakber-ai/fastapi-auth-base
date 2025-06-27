# --- MODULE IMPORTS ---
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field

class Settings(BaseSettings):
    # Model for pydantic to read settings from environment variables
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True, # Ensure that variable names are case sensitive
        extra="ignore", # Ignore extra fields not defined in the model
    )

    # Database Settings
    DATABASE_URL: PostgresDsn = Field(
        ...,
        env="DATABASE_URL",
        description="The postgreSQL database connection URL (e.g., postgresql://user:password@host:port/dbname)"
    )

    # Application Metadata
    PROJECT_NAME: str = Field(
        "Learnobots Job Portal API",
        env="PROJECT_NAME",
        description="Name of the FastAPI project"
    )
    API_V1_STR: str = Field(
        "/api/v1",
        env="API_V1_STR",
        description="Base path for API version 1 endpoints."
    )

settings = Settings()

print(f"Loading settings for: {settings.PROJECT_NAME}")
print(f"API Base Path: {settings.API_V1_STR}")