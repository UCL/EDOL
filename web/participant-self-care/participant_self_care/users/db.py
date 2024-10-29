import os
from collections.abc import AsyncGenerator
from threading import Lock

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


class DbEngine:
    _engine: AsyncEngine | None = None
    _async_session_maker: async_sessionmaker[AsyncSession] | None = None

    _lock: Lock = Lock()

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        print("get_engine")
        if DbEngine._engine is None:
            DATABASE_URL = os.getenv(
                "DATABASE_URL", "sqlite+aiosqlite:///./users.sqlite"
            )
            DbEngine._engine = create_async_engine(DATABASE_URL)
        return DbEngine._engine

    @classmethod
    def get_async_session_maker(cls) -> async_sessionmaker[AsyncSession]:
        print("get_async_session_maker")
        if DbEngine._async_session_maker is None:
            DbEngine._async_session_maker = async_sessionmaker(
                cls.get_engine(), expire_on_commit=False
            )
        return DbEngine._async_session_maker


async def create_db_and_tables() -> None:
    engine = DbEngine.get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = DbEngine.get_async_session_maker()
    async with async_session() as session:
        yield session


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[User, User], None]:
    yield SQLAlchemyUserDatabase(session, User)
