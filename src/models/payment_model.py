from uuid import UUID
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.config import settings
from models.spent_model import SpentModel


class PaymentModel(settings.DBBaseModel):
    __tablename__ = 'payment'

    payment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    name = Column(String(256), nullable=False, unique=True)
    description = Column(String(256), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.user_id'), nullable=False)
    share = Column(Boolean, nullable=False, default=True)
    active = Column(Boolean, nullable=False, default=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())
    
    spent = relationship(SpentModel, backref='payment')
