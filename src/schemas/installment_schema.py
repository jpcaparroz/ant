from datetime import datetime
from datetime import date as dt
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseInstallmentSchema(BaseModel):
    spent_id: UUID
    number: int
    amount: int
    due_date: dt
    value: float
    paid: bool


class UpdateInstallmentSchema(BaseInstallmentSchema):
    spent_id: Optional[UUID] = None
    number: Optional[int] = None
    amount: Optional[int] = None
    due_date: Optional[dt] = None
    value: Optional[float] = None
    paid: Optional[bool] = None


class GetInstallmentSchema(BaseInstallmentSchema):
    installment_id: Optional[UUID] = None
    created_on: datetime
    updated_on: Optional[datetime] = None
