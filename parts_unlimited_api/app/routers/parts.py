from app.api.api_v1.endpoints import parts
from fastapi import APIRouter

part_router = APIRouter()
part_router.include_router(
    parts.router,
    prefix="/parts",
    tags=["parts"],
)
