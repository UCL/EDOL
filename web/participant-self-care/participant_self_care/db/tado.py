import time
from uuid import UUID
from participant_self_care.core.config import Config
from participant_self_care.core.security import get_cipher
from participant_self_care.db.session import Base
from sqlalchemy.ext.asyncio import AsyncSession
from participant_self_care.schemas.users import TadoCredentialsCreate
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer, String, select, update

from tadoclient.client import TadoClient
from tadoclient.models import TadoToken


class TadoCredentials(Base):
    __tablename__ = "tado_credentials"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = Column(String, ForeignKey("user.id"), unique=True)
    _refresh_token = Column("refresh_token", String, nullable=False)
    _access_token = Column("access_token", String, nullable=True)
    expires_at = Column(Integer, nullable=True)

    user = relationship("User", back_populates="tado_credentials")

    def __init__(self, **kwargs) -> None:  # type: ignore
        if "user_id" in kwargs:
            kwargs["user_id"] = str(kwargs["user_id"])

        if "refresh_token" in kwargs:
            kwargs["_refresh_token"] = (
                get_cipher().encrypt(kwargs.pop("refresh_token").encode()).decode()
            )
        if "access_token" in kwargs:
            kwargs["_access_token"] = (
                get_cipher().encrypt(kwargs.pop("access_token").encode()).decode()
            )
        from rich import print

        super().__init__(**kwargs)

    @hybrid_property
    def refresh_token(self):
        print("refresh_token", self._refresh_token)
        if self._refresh_token:
            return get_cipher().decrypt(self._refresh_token.encode()).decode()
        return None

    @refresh_token.setter  # type: ignore
    def refresh_token(self, value):
        print("refresh_token SET", value)
        if value:
            self._refresh_token = get_cipher().encrypt(value.encode()).decode()
        else:
            self._refresh_token = None

    @hybrid_property
    def access_token(self):
        if self._access_token:
            return get_cipher().decrypt(self._access_token.encode()).decode()
        return None

    @access_token.setter  # type: ignore
    def access_token(self, value):
        if value:
            self._access_token = get_cipher().encrypt(value.encode()).decode()
        else:
            self._access_token = None


async def upsert_tado_credentials(
    db: AsyncSession, user_id: str, credentials: TadoCredentialsCreate
) -> TadoCredentials:
    # First try to update existing record
    update_stmt = (
        update(TadoCredentials)
        .where(TadoCredentials.user_id == user_id)
        .values(
            refresh_token=credentials.refresh_token,
            access_token=credentials.access_token,
            expires_at=credentials.expires_at,
        )
    )
    update_result = await db.execute(update_stmt)

    # If no rows were updated (didn't exist), then insert
    if update_result.rowcount == 0:
        db_credentials = TadoCredentials(
            user_id=user_id,
            refresh_token=credentials.refresh_token,
            access_token=credentials.access_token,
            expires_at=credentials.expires_at,
        )
        db.add(db_credentials)

    await db.commit()

    # Fetch and return the final record
    select_result = await db.execute(
        select(TadoCredentials).where(TadoCredentials.user_id == user_id)
    )
    db_credentials = select_result.scalar_one()
    return db_credentials


class TadoNoCredentialsError(Exception):
    pass


async def get_tado_credentials(
    db: AsyncSession, user_id: UUID, config: Config
) -> TadoCredentials | None:
    stmt = select(TadoCredentials).where(TadoCredentials.user_id == str(user_id))
    result = await db.execute(stmt)
    tado_credentials = result.scalar_one_or_none()

    if tado_credentials is None:
        raise TadoNoCredentialsError(f"No Tado credentials found for user {user_id}")
    print(
        "tado_credentials",
        tado_credentials.expires_at,
        time.time(),
        tado_credentials.expires_at - time.time(),
    )

    if tado_credentials.expires_at < time.time():
        tadoclient = TadoClient.get_client(
            TadoToken(
                refresh_token=tado_credentials.refresh_token,
                access_token=tado_credentials.access_token,
                expires_at=tado_credentials.expires_at,
            ),
            config.tado,
        )

        new_token: TadoToken = await tadoclient.refresh_token()

        # tado_credentials = await upsert_tado_credentials(
        #     db=db,
        #     user_id=str(user_id),
        #     credentials=TadoCredentialsCreate(
        #         refresh_token=new_token.refresh_token,
        #         access_token=new_token.access_token,
        #         expires_at=new_token.expires_at,
        #     ),
        # )

    return tado_credentials
