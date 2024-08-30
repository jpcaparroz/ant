from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BasePaymentSchema(BaseModel):
    name: str
    description: str
    user_id: UUID
    share: bool = True
    active: bool = True


class CreatePaymentSchema(BasePaymentSchema):
    description: Optional[str] = None


class UpdatePaymentSchema(BasePaymentSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    share: Optional[bool] = None
    active: Optional[bool] = None


class GetPaymentSchema(BasePaymentSchema):
    payment_id: UUID
    description: Optional[str] = None
    created_on: datetime
    updated_on: Optional[datetime] = None
