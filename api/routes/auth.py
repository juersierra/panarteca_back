__all__: list[str] = ["auth_router"]

from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic_mongo import PydanticObjectId

from ..models.users import CreationUser, LoginUser
from ..services.auth import AuthCredentials, UsersServiceDependency

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
def register(user: CreationUser, auth: UsersServiceDependency):
    inserted_id = auth.create_one(user)
    return {"result message": f"User created with id: {inserted_id}"}


@auth_router.post("/login")
def login_with_cookie(
    user: LoginUser,
    response: Response,
    auth: UsersServiceDependency,
):
    return auth.login_and_set_access_token(user, response)


@auth_router.get("authenticated_user")
def read_current_user(credentials: AuthCredentials):
    return credentials.subject
