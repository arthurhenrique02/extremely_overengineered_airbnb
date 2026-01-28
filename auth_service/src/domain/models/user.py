from datetime import datetime
from typing import Annotated

from pydantic import UUID4, BaseModel, EmailStr, Field


class User(BaseModel):
    id: UUID4

    name: Annotated[str, Field(min_length=1, max_length=100)]
    surname: Annotated[str, Field(min_length=1, max_length=100)]
    birth_date: Annotated[datetime, Field()]

    email: EmailStr
    username: Annotated[str, Field(min_length=3, max_length=50)]
    password: Annotated[str, Field(description="The hashed password of the user")]

    is_superuser: Annotated[bool, Field()] = False

    is_active: Annotated[bool, Field()] = False
    created_at: Annotated[datetime, Field()]
    updated_at: Annotated[datetime, Field()]

    class Config:
        orm_mode = True
