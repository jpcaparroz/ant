from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import field_validator
from pydantic import EmailStr

from core.security import generate_hash


class BaseUserSchema(BaseModel):
    name: str
    email: EmailStr
    is_admin: bool = False
    active: bool = True


class CreateUserSchema(BaseUserSchema):
    password: str

    @field_validator("password", mode='before')
    def hash_password(cls, value) -> str:
        return generate_hash(value)


class UpdateUserSchema(BaseUserSchema):
    name: Optional[str] = None
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_admin: Optional[bool] = None
    active: Optional[bool] = None

    @field_validator("password", mode='before')
    def hash_password(cls, value) -> str:
        return generate_hash(value)


class GetUserSchema(BaseUserSchema):
    user_id: UUID
    created_on: datetime
    updated_on: Optional[datetime] = None

