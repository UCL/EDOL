from pathlib import Path
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from participant_self_care.core.config import config
from participant_self_care.db.tado import get_tado_credentials
from sqlalchemy.ext.asyncio import AsyncSession

from participant_self_care.db.users import User
from participant_self_care.services.auth import current_active_user
from participant_self_care.db.session import get_async_session
from tadoclient.client import TadoClient
from tadoclient.models import TadoToken


router = APIRouter()
partials = Jinja2Templates(
    directory=Path(__file__).parent.parent / "templates" / "partials" / "tado"
)


@router.get("/status")
async def status(
    request: Request,
    active_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
) -> Response:
    tado_credentials = await get_tado_credentials(db, active_user.id, config)
    import time

    print(tado_credentials.expires_at - time.time())
    if not tado_credentials:
        return HTMLResponse("<a href='/tado/login'>Authorize</a>")

    return partials.TemplateResponse("card.html", {"request": request})
