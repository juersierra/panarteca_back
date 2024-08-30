__all__ = [
    "BaseUser",
    "CreationUserCustomer",
    "CreationUserArtist",
    "LoginUser",
    "PublicStoredUser",
    "PrivateStoredUser",
    "CreateUserArtistAndArtist",
    "CreationUserAdmin",
]

from enum import Enum

from pydantic import AliasChoices, BaseModel, Field
from pydantic_mongo import PydanticObjectId
from .artists import CreateArtist


class Role(str, Enum):
    admin = "admin"
    artist = "artist"
    customer = "customer"


class CreationRole(str, Enum):
    customer = "customer"
    artist = "artist"


class BaseUser(BaseModel):
    username: str
    email: str
    role: Role


class CreationUserCustomer(BaseUser):
    role: CreationRole = CreationRole.customer
    password: str


class CreationUserArtist(BaseUser):
    role: CreationRole = CreationRole.artist
    password: str


class CreationUserAdmin(BaseUser):
    role: Role = Role.admin
    password: str


class CreateUserArtistAndArtist(CreationUserArtist, CreateArtist):
    pass


class LoginUser(BaseModel):
    username: str
    password: str


class PublicStoredUser(BaseUser):
    id: PydanticObjectId = Field(validation_alias=AliasChoices("_id", "id"))


class PrivateStoredUser(BaseUser):
    id: PydanticObjectId = Field(alias="_id")
    hash_password: str
