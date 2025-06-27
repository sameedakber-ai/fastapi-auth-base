from datetime import datetime
from pydantic import BaseModel, Field
from typing import List

class UserBase(BaseModel):
    email: str = Field(
        ...,
        description="USer email"
    )

class UserCreate(UserBase):
    password: str = Field(
        ...,
        description="Plain password input from the user"
    )

class UserInDBBase(UserBase):
    class Config:
        from_attributes = True

    id: int = Field(
        ...,
        description="Unique identifier for the user"
    )
    hashed_password: str = Field(
        ...,
        description="The bcrypt hash of the user password"
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user is currently active"
    )
    role: str = Field(
        default="user",
        description="The role of the user, i.e. user, hr, admin etc."
    )
    created_at: datetime = Field(
        ...,
        description="Time and date for when the user was created"
    )
    updated_at: datetime = Field(
        ...,
        description="Date and time for when the user object was last updated"
    )

class User(UserInDBBase):
    class Config:
        from_attributes = True

