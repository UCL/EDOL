from fastapi import APIRouter

from participant_self_care.web.htmx.tado import router as tado_router

router = APIRouter()

router.include_router(tado_router, prefix="/tado", tags=["tado"])
