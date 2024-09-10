__all__ = [
    "BaseUser",
    "CreationUserCustomer",
    "CreationUserArtist",
    "LoginUser",
    "CreationUser",
    "PublicStoredUser",
    "PrivateStoredUser",
    "CreateUserArtistAndArtist",
    "CreationUserAdmin",
]

from enum import Enum

from pydantic import AliasChoices, BaseModel, Field
from pydantic_mongo import PydanticObjectId
from .artists import Artist


class Role(str, Enum):
    admin = "admin"
    artist = "artist"
    customer = "customer"


class CreationRole(str, Enum):
    customer = "customer"
    artist = "artist"


class User(BaseModel):
    username: str
    email: str


class BaseUser(User):
    role: Role


class CreationUser(User):
    password: str


class CreationUserCustomer(User):
    hash_password: str
    role: CreationRole = CreationRole.customer


class CreationUserArtist(User):
    hash_password: str
    role: CreationRole = CreationRole.artist


class CreationUserAdmin(User):
    hash_password: str
    role: Role = Role.admin


class CreateUserArtistAndArtist(CreationUser, Artist):
    pass


class LoginUser(BaseModel):
    username: str
    password: str


class PublicStoredUser(BaseUser):
    id: PydanticObjectId = Field(validation_alias=AliasChoices("_id", "id"))


class PrivateStoredUser(BaseUser):
    id: PydanticObjectId = Field(alias="_id")
    hash_password: str
