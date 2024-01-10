from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import settings

from src.auth.models import User


SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{settings.SQLITE_DB}"

# Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,echo="debug")
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

