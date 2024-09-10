from fastapi import APIRouter

from .orders import order_router
from .auth import auth_router
from .artwork import artwork_router
from .users import users_router

__all__: list[str] = ["api_router"]

api_router = APIRouter(prefix="/api")
api_router.include_router(artwork_router)
api_router.include_router(users_router)
api_router.include_router(order_router)
