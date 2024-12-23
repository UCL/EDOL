import uuid
from typing import List

from fastapi_users import schemas
from pydantic import BaseModel


class TadoCredentialsCreate(BaseModel):
    refresh_token: str | None = None
    access_token: str | None = None
    expires_at: int | None = None


class UserRead(schemas.BaseUser[uuid.UUID]):
    roles: List[str] = []
    hildebrand_user_id: str | None = None


class UserCreate(schemas.BaseUserCreate):
    roles: List[str] = []
    hildebrand_user_id: str | None = None


class UserUpdate(schemas.BaseUserUpdate):
    roles: List[str] = []
    hildebrand_user_id: str | None = None
