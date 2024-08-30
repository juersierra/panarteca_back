__all__ = ["Artwork", "UpdateArtwork", "StoredArtwork", "BaseArtwork"]

from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId


class Artwork(BaseModel):
    name: str
    description: str
    technique: str
    year: int
    price: float
    serie: str
    sold: bool = False
    artist_id: PydanticObjectId


class BaseArtwork(BaseModel):
    name: str
    description: str
    technique: str
    year: int
    price: float
    serie: str


class UpdateArtwork(BaseModel):
    name: str = Field(default=None)
    description: str = Field(default=None)
    technique: str = Field(default=None)
    year: int = Field(default=None)
    price: float = Field(default=None)
    serie: str = Field(default=None)
    collection_id: PydanticObjectId = Field(default=None)


class StoredArtwork(BaseArtwork):
    id: PydanticObjectId = Field(alias="_id")
    sold: bool
    artist_id: PydanticObjectId
