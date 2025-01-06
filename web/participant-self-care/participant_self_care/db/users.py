import os
from collections.abc import AsyncGenerator


from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from participant_self_care.core.security import get_cipher
from participant_self_care.db.session import Base, get_async_session
from participant_self_care.schemas.users import TadoCredentialsCreate
from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


User.tado_credentials = relationship(
    "TadoCredentials", back_populates="user", uselist=False
)


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase[User, User], None]:
    yield SQLAlchemyUserDatabase(session, User)
