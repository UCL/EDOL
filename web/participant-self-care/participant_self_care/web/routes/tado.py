import time
from typing import Any

from authlib.integrations.starlette_client import OAuthError
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from participant_self_care.db.session import get_async_session
from participant_self_care.db.tado import upsert_tado_credentials
from participant_self_care.db.users import User
from participant_self_care.decorators.tado_decorator import require_tado_auth
from participant_self_care.schemas.users import TadoCredentialsCreate
from participant_self_care.services.auth import current_active_user
from participant_self_care.services.tado import tado_oauth
from participant_self_care.core.config import config
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/login")
async def tado_login(request: Request) -> Any:
    redirect_uri = config.tado.redirect_uri
    return await tado_oauth.tado.authorize_redirect(request, redirect_uri)


@router.get("/logout")
async def logout(request: Request) -> Response:
    request.session.pop("tado_token", None)
    return RedirectResponse(url="/")


@router.get("/auth")
async def auth(
    request: Request,
    db: AsyncSession = Depends(get_async_session),
    active_user: User = Depends(current_active_user),
) -> Response:
    try:
        token = await tado_oauth.tado.authorize_access_token(request)
    except OAuthError as error:
        print(error)
        return HTMLResponse(f"<h1>{error.error}</h1>")

    if token:
        # Calculate expiry time
        expires_at = int(token.get("expires_in", 0) + time.time())

        # Create credentials object with proper fields
        credentials = TadoCredentialsCreate(
            refresh_token=token["refresh_token"],
            access_token=token["access_token"],
            expires_at=expires_at,
        )

        # Store in database
        try:
            await upsert_tado_credentials(db, active_user.id, credentials)
        except Exception as e:
            print(f"Failed to store credentials: {e}")
            return HTMLResponse("<h1>Failed to store credentials</h1>")

    return RedirectResponse(url="/", status_code=303)
