import pathlib
import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Dict

from authlib.integrations.starlette_client import OAuth, OAuthError
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Response
from fastapi.staticfiles import StaticFiles
from participant_self_care.tado_decorator import require_tado_auth
from participant_self_care.users.db import User, create_db_and_tables
from participant_self_care.users.schemas import UserCreate, UserRead, UserUpdate
from participant_self_care.users.users import (
    auth_backend,
    current_active_user,
    fastapi_users,
)
from rich import print
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from tadoclient.client import TadoClient
from tadoclient.models import TadoClientConfig, TadoToken


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_db_and_tables()
    yield


load_dotenv()

config = Config(".env")

app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=config("TADO_OAUTH_APP_SECRET"))

### USERS

PARTICIPANT_PATH_PREFIX = "/participant"
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"{PARTICIPANT_PATH_PREFIX}/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f"{PARTICIPANT_PATH_PREFIX}/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=f"{PARTICIPANT_PATH_PREFIX}/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix=f"{PARTICIPANT_PATH_PREFIX}/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix=f"{PARTICIPANT_PATH_PREFIX}/users",
    tags=["users"],
)

### TADO
tado_oauth = OAuth(config)


tado_config = TadoClientConfig(
    client_id=config("TADO_CLIENT_ID"),
    client_secret=config("TADO_CLIENT_SECRET"),
    api_base_url=config("TADO_API_BASE_URL"),
    refresh_token_url=config("TADO_REFRESH_TOKEN_URL"),
    authorize_url=config("TADO_AUTHORIZE_URL"),
    access_token_url=config("TADO_TOKEN_URL"),
)

tado_oauth.register(**tado_config.model_dump())


@app.get("/tado/dashboard")
@require_tado_auth(tado_config=tado_config)
async def homepage(request: Request) -> Response:
    tadoclient = request.state.tadoclient
    me = await tadoclient.populated_user()
    html = f"<pre>{me.model_dump_json(indent=4)}</pre>" '<a href="/logout">logout</a>'
    return HTMLResponse(html)


@app.get("/tado/login")
async def tado_login(request: Request) -> Any:
    redirect_uri = config("TADO_REDIRECT_URI")
    return await tado_oauth.tado.authorize_redirect(request, redirect_uri)


@app.get("/tado/auth")
async def auth(request: Request) -> Response:
    try:
        token = await tado_oauth.tado.authorize_access_token(request)
        print(token)
    except OAuthError as error:
        print(error)
        return HTMLResponse(f"<h1>{error.error}</h1>")
    if token:
        token["expires_at"] = int(token.get("expires_in", 0) + time.time())
        request.session["tado_token"] = TadoToken(**token).model_dump()
    return RedirectResponse(url="/")


@app.get("/")
async def dashboard(
    user: User = Depends(current_active_user),
) -> Response:
    return HTMLResponse(f"Hello, {user.email}!")


@app.get("/login")
async def login() -> Response:
    login_path = pathlib.Path(__file__).parent / "static" / "login.html"
    with open(login_path) as f:
        return HTMLResponse(f.read())


@app.get("/logout")
async def logout(request: Request) -> Response:
    request.session.pop("tado_token", None)
    return RedirectResponse(url="/")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
