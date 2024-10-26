from uuid import UUID
from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy import SmallInteger
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Date
from sqlalchemy import UUID
from sqlalchemy.sql import func

from core.config import settings

class SpentModel(settings.DBBaseModel):
    __tablename__ = 'spent'

    spent_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    date = Column(Date, nullable=False, unique=False)
    name = Column(String(256), nullable=False, unique=False)
    description = Column(String(256), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id'), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey('category.category_id'), nullable=False)
    payment_id = Column(UUID(as_uuid=True), ForeignKey('payment.payment_id'), nullable=False)
    installment_quantity = Column(SmallInteger, nullable=True, default=0)
    installment_value = Column(Float, nullable=True, default=0)
    value = Column(Float, nullable=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())

    installment = relationship("InstallmentModel", back_populates="spent", cascade="all, delete-orphan")
