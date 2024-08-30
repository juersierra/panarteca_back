__all__: list[str] = ["auth_router"]

from fastapi import Response
from fastapi.routing import APIRouter


from ..models import LoginUser
from ..services import UsersServiceDependency, AuthServiceDependency, SecurityDependency

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
def login_with_cookie(
    user: LoginUser,
    response: Response,
    users: UsersServiceDependency,
    auth: AuthServiceDependency,
):
    db_user = users.get_one(username=user.username, with_password=True)
    return auth.login_and_set_access_token(
        user=user, db_user=db_user, response=response
    )


@auth_router.get("/authenticated_user")
def read_current_user(security: SecurityDependency):
    return dict(
        id=security.auth_user_id,
        username=security.auth_user_username,
        email=security.auth_user_email,
        role=security.auth_user_role,
    )
