import time
from typing import Any

from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import FastAPI, Response
from rich import print
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from tadoclient.client import TadoClient
from tadoclient.models import TadoClientConfig, TadoToken

config = Config(".env")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=config("TADO_OAUTH_APP_SECRET"))

oauth = OAuth(config)

tado_config = TadoClientConfig(
    client_id=config("TADO_CLIENT_ID"),
    client_secret=config("TADO_CLIENT_SECRET"),
    api_base_url=config("TADO_API_BASE_URL"),
    refresh_token_url=config("TADO_REFRESH_TOKEN_URL"),
    authorize_url=config("TADO_AUTHORIZE_URL"),
    access_token_url=config("TADO_TOKEN_URL"),
)

oauth.register(**tado_config.model_dump())


@app.get("/")
async def homepage(request: Request) -> Response:
    token = request.session.get("token")
    if token:
        tadoclient = TadoClient.get_client(TadoToken(**token), tado_config)
        me = await tadoclient.populated_user()
        html = (
            f"<pre>{me.model_dump_json(indent=4)}</pre>" '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login">login</a>')


@app.get("/login")
async def login(request: Request) -> Any:
    redirect_uri = config("TADO_REDIRECT_URI")
    return await oauth.tado.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request) -> Response:
    try:
        token = await oauth.tado.authorize_access_token(request)
        print(token)
    except OAuthError as error:
        print(error)
        return HTMLResponse(f"<h1>{error.error}</h1>")
    if token:
        token["expires_at"] = int(token.get("expires_in", 0) + time.time())
        request.session["token"] = TadoToken(**token).model_dump()
    return RedirectResponse(url="/")


@app.get("/me")
async def me(request: Request) -> Response:
    """
    A deug route to show the user information. To be refres
    FIXME: do this with decorators for tadoclient
    """
    token = request.session.get("token")
    if token:
        tadoclient = TadoClient.get_client(TadoToken(**token), tado_config)
        if tadoclient.token.expires_at < time.time():
            new_token = await tadoclient.refresh_token()
            request.session["token"] = new_token.model_dump()

        me = await tadoclient.get_user()

        token_expires_date = time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime(tadoclient.token.expires_at)
        )
        refresh_token_expires_date = time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(tadoclient.token.expires_at + 365 * 24 * 60 * 60),
        )
        html = (
            f"<pre>{me.model_dump_json(indent=4)}</pre>"
            f"<p>Token expires at: {token_expires_date}</p>"
            f"<p>Refresh token expires at: {refresh_token_expires_date}</p>"
        )
        return HTMLResponse(html)
    return RedirectResponse(url="/login")


@app.get("/logout")
async def logout(request: Request) -> Response:
    request.session.pop("token", None)
    return RedirectResponse(url="/")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
