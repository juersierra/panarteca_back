from fastapi import APIRouter
from .artwork import artwork_router
from .auth import auth_router

__all__: list[str] = ["api_router"]

api_router = APIRouter(prefix="/api")
api_router.include_router(artwork_router)
api_router.include_router(auth_router)
