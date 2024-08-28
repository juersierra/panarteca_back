__all__ = [
    "Artist",
    "PublicUpdateArtist",
    "PrivateUpdateArtist",
    "CreateArtist",
    "PublicStoredArtist",
    "PrivateStoredArtist",
]

from pydantic import BaseModel, ConfigDict, Field
from pydantic_mongo import PydanticObjectId


class Artist(BaseModel):
    name: str
    pseudo: str
    description: str
    image: str = Field(default=None)


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


class CreateArtist(Artist):
    commision: int = 15
    model_config = ConfigDict(extra="ignore")


class PublicStoredArtist(Artist):
    id: PydanticObjectId = Field(alias="_id")


class PrivateStoredArtist(Artist):
    id: PydanticObjectId = Field(alias="_id")
    commision: int
