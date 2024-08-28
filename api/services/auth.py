__all__ = ["AuthServiceDependency", "SecurityDependency", "AuthService"]

from typing import Annotated

from fastapi import Depends, HTTPException, Response, Security, status
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from passlib.context import CryptContext

from ..config import token_expiration_time, SECRET_KEY
from ..models import LoginUser, PublicStoredUser

jwt_bearer = JwtAccessBearer(secret_key=SECRET_KEY or "", auto_error=True)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

AuthCredentials = Annotated[JwtAuthorizationCredentials, Security(jwt_bearer)]


class AuthService:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    def login_and_set_access_token(
        self, db_user: dict | None, user: LoginUser, response: Response
    ):
        if not db_user or not self.verify_password(
            user.password, db_user.get("hash_password")
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credentials incorrect",
            )
        print(db_user)
        userdata = PublicStoredUser.model_validate(db_user).model_dump()
        access_token = jwt_bearer.create_access_token(
            subject=userdata, expires_delta=token_expiration_time
        )
        jwt_bearer.set_access_cookie(response, access_token)

        return {"access_token": access_token}


class SecurityService:
    def __init__(self, credentials: AuthCredentials):
        self.auth_user_id = credentials.subject.get("id")
        self.auth_user_username = credentials.subject.get("username")
        self.auth_user_email = credentials.subject.get("email")
        self.auth_user_role = credentials.subject.get("role")

    @property
    def is_admin(self):
        return self.auth_user_role == "admin"

    @property
    def is_customer(self):
        return self.auth_user_role == "customer"

    @property
    def is_artist(self):
        return self.auth_user_role == "artist"

    @property
    def is_admin_or_raise(self):
        assert self.auth_user_role == "admin", "User does not have admin role"

    @property
    def is_artist_or_raise(self):
        role = self.auth_user_role
        assert role == "admin" or role == "artist", "User does not have artist role"

    @property
    def is_customer_or_raise(self):
        role = self.auth_user_role
        assert role == "admin" or role == "customer", "User does not have customer role"


AuthServiceDependency = Annotated[AuthService, Depends()]
SecurityDependency = Annotated[SecurityService, Depends()]
