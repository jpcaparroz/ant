from datetime import datetime
from datetime import date as dt
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseSpentSchema(BaseModel):
    date: dt
    name: str
    description: str
    user_id: UUID
    category_id: UUID
    payment_id: UUID
    value: float


class CreateSpentSchema(BaseSpentSchema):
    description: Optional[str] = None
    installment_quantity: Optional[int] = None


class UpdateSpentSchema(BaseSpentSchema):
    date: Optional[dt] = None
    name: Optional[str] = None
    description: Optional[str] = None
    user_id: Optional[UUID]
    category_id: Optional[UUID]
    payment_id: Optional[UUID]
    installment_quantity: Optional[int] = None
    installment_value: Optional[float] = None
    value: Optional[float] = None


class GetSpentSchema(BaseSpentSchema):
    spent_id: UUID
    description: Optional[str] = None
    installment_quantity: Optional[int] = None
    installment_value: Optional[float] = None
    created_on: datetime
    updated_on: Optional[datetime] = None


class GetTreatedSpentSchema(BaseModel):
    date: dt
    name: str
    description: Optional[str] = None
    installment_quantity: Optional[int] = None
    installment_value: Optional[float] = None
    value: float
    
    # Category join
    category_name: Optional[str] = None
    
    # Payment join
    payment_name: Optional[str] = None

    class Config:
        from_attributes = True
