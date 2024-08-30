from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseCategorySchema(BaseModel):
    name: str
    description: str
    user_id: UUID
    share: bool = True
    active: bool = True


class CreateCategorySchema(BaseCategorySchema):
    description: Optional[str] = None


class UpdateCategorySchema(BaseCategorySchema):
    name: Optional[str] = None
    description: Optional[str] = None
    share: Optional[bool] = None
    active: Optional[bool] = None


class GetCategorySchema(BaseCategorySchema):
    category_id: UUID
    description: Optional[str] = None
    created_on: datetime
    updated_on: Optional[datetime] = None
