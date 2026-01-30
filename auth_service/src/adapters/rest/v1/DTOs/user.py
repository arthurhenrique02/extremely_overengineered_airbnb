from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    birth_date: str = Field(..., description="Birth date in ISO format (YYYY-MM-DD)")
    email: EmailStr = Field(...)
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Arthur",
                "surname": "Henrique",
                "birth_date": "1990-01-15",
                "email": "arthur.henrique@example.com",
                "username": "arthurhenrique",
                "password": "secure_password_123",
            }
        }


class UserAuthRequest(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "arthur.henrique@example.com",
                "password": "secure_password_123",
            }
        }


class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, description="User's first name"
    )
    surname: Optional[str] = Field(
        None, min_length=1, max_length=100, description="User's last name"
    )
    email: Optional[EmailStr] = Field(None, description="User's email address")
    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Unique username"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rayssa",
                "surname": "Leal",
                "email": "rayssa.leal@example.com",
                "username": "rayssaleal",
            }
        }


class UserResponse(BaseModel):
    id: UUID4
    name: str
    surname: str
    birth_date: datetime
    email: str
    username: str
    is_superuser: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "Arthur",
                "surname": "Henrique",
                "birth_date": "1990-01-15T00:00:00",
                "email": "arthur.henrique@example.com",
                "username": "arthurhenrique",
                "is_superuser": False,
                "is_active": True,
                "created_at": "2024-01-28T10:00:00",
                "updated_at": "2024-01-28T10:00:00",
            }
        }
