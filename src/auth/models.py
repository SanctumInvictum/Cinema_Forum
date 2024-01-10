import uuid
from datetime import datetime

# from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text, Integer
from sqlalchemy.dialects.postgresql import UUID
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import relationship, DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    # role_id = Column(Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)

