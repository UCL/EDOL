# web/routes/dashboard.py - Renders full HTML pages
from pathlib import Path

from fastapi import APIRouter, Depends, Request, Response
from fastapi.templating import Jinja2Templates
from participant_self_care.db.users import User
from participant_self_care.services.auth import current_user

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


@router.get("/")
async def dashboard_page(
    request: Request,
    user: User = Depends(current_user),
) -> Response:
    if user is None:
        return templates.TemplateResponse("login.html", {"request": request})
    return templates.TemplateResponse("dashboard/index.html", {"request": request})
