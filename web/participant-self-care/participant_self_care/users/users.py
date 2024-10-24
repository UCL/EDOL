from collections.abc import AsyncGenerator
import uuid
import os
from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from participant_self_care.users.db import User, get_user_db


def get_jwt_secret() -> str:
    secret = os.getenv("EDOL_PP_SELF_CARE_JWT_SECRET")
    if secret is None:
        raise ValueError("EDOL_PP_SELF_CARE_JWT_SECRET must be set")
    return secret


class JWTSecret:
    def __get__(self, _: object, __: object) -> str:
        return get_jwt_secret()


# I had to work around the reset_password_token_secret and verification_token_secret properties being
# properties initialized by a SECRET that was hardcoded (cdinu, 24/10/202)
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = JWTSecret()  # type: ignore
    verification_token_secret = JWTSecret()  # type: ignore

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ) -> None:
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        print(f"User {user.id} has logged in.")
        return await super().on_after_login(user, request, response)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


bearer_transport = CookieTransport(
    cookie_name="edolauth",
    cookie_max_age=3600,
)


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:
    return JWTStrategy(
        secret=get_jwt_secret(), token_audience="edol:auth", lifetime_seconds=3600
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)
