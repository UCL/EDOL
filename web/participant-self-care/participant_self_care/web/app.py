import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from participant_self_care.core.config import config
from participant_self_care.db.session import create_db_and_tables
from participant_self_care.web.routes.auth import router as auth_router
from participant_self_care.web.routes.dashboard import router as dashboard_router
from participant_self_care.web.routes.status import router as status_router
from participant_self_care.web.routes.tado import router as tado_router
from participant_self_care.web.htmx import router as htmx_router
from starlette.middleware.sessions import SessionMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_db_and_tables()
    yield


logger = config.logger

app = FastAPI(lifespan=lifespan)
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)

app.add_middleware(SessionMiddleware, secret_key=config.edol_pp_self_care_sess_secret)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tado_router, prefix="/tado", tags=["tado"])
app.include_router(status_router, prefix="/status", tags=["status"])
app.include_router(dashboard_router, prefix="", tags=["dashboard"])

app.include_router(htmx_router, prefix="/htmx", tags=["htmx"])


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("EDOL_PP_SELF_CARE_PORT", 8000))
    config.logger.debug("Starting app", port=port)
    uvicorn.run(app, host="127.0.0.1", port=port)
