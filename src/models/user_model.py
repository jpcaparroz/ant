from uuid import UUID
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import UUID
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.config import settings
from models.category_model import CategoryModel
from models.payment_model import PaymentModel
from models.spent_model import SpentModel


class UserModel(settings.DBBaseModel):
    __tablename__ = 'user'

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True)
    name = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True)
    password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    active = Column(Boolean, nullable=False, default=True)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship(CategoryModel, backref='user')
    payment = relationship(PaymentModel, backref='user')
    spent = relationship(SpentModel, backref='user')