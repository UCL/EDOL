from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/")
async def status() -> str:
    return "OK"
