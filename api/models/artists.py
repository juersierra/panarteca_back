__all__ = [
    "Artist",
    "CreateArtist",
    "PublicUpdateArtist",
    "PrivateUpdateArtist",
    "PublicStoredArtist",
    "PrivateStoredArtist",
]

from pydantic import BaseModel, ConfigDict, Field
from pydantic_mongo import PydanticObjectId


class Artist(BaseModel):
    name: str
    pseudo: str
    description: str
    image: str | None = Field(default=None)
    user_id: PydanticObjectId


class CreateArtist(BaseModel):
    name: str
    pseudo: str
    description: str
    image: str | None = Field(default=None)


class PublicUpdateArtist(BaseModel):
    name: str = Field(default=None)
    pseudo: str = Field(default=None)
    description: str = Field(default=None)
    image: str = Field(default=None)


class PrivateUpdateArtist(BaseModel):
    name: str = Field(default=None)
    pseudo: str = Field(default=None)
    description: str = Field(default=None)
    image: str = Field(default=None)
    commision: int = Field(default=None)


class PublicStoredArtist(Artist):
    id: PydanticObjectId = Field(alias="_id")


class PrivateStoredArtist(Artist):
    id: PydanticObjectId = Field(alias="_id")
    commision: int
