import uuid
from datetime import datetime

# from .database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Boolean, text, Integer
from sqlalchemy.dialects.postgresql import UUID
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import relationship, DeclarativeMeta, declarative_base

from src.auth.models import User

Base: DeclarativeMeta = declarative_base()


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    title = Column(String)
    content = Column(String)
    # category = Column(String)
    image = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    likes_count = Column(Integer)
    comments_count = Column(Integer)

    user = relationship(User)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)


class PostCategories(Base):
    __tablename__ = 'post_categories'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey(Post.id))
    category_id = Column(Integer, ForeignKey(Category.id))

    post = relationship(Post)
    category = relationship(Category)