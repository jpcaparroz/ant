from uuid import UUID
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import UUID
from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from core.config import settings


class UserModel(settings.DBBaseModel):
    __tablename__ = 'user'
    
    id = Column(Integer(), primary_key=True, autoincrement=True, unique=True)
    user_uuid = Column(UUID(as_uuid=True), default=uuid4, unique=True)
    user_name = Column(String(256), nullable=False)
    user_email = Column(String(256), nullable=False, unique=True)
    user_password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_on = Column(DateTime(timezone=True), server_default=func.now())
    updated_on = Column(DateTime(timezone=True), onupdate=func.now())

