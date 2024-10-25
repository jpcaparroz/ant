from uuid import UUID
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Boolean
from sqlalchemy import SmallInteger
from sqlalchemy import UUID
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

from core.config import settings


class InstallmentModel(settings.DBBaseModel):
    __tablename__ = 'installment'

    installment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    spent_id = Column(UUID(as_uuid=True), ForeignKey('spent.spent_id'), nullable=False)
    number = Column(SmallInteger, nullable=True, default=0)
    amount = Column(SmallInteger, nullable=True, default=0)
    due_date = Column(Date, nullable=False, unique=False)
    value = Column(Float, nullable=False)
    paid = Column(Boolean, nullable=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())
