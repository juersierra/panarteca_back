__all__ = ["Artwork", "UpdateArtwork", "StoredArtwork", "BaseArtwork"]

from typing import Optional
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
    name: None | str = Field(default=None)
    description: None | str = Field(default=None)
    technique: None | str = Field(default=None)
    year: None | int = Field(default=None)
    price: None | float = Field(default=None)
    serie: None | str = Field(default=None)
    # collection_id: PydanticObjectId = Field(default=None)


class StoredArtwork(Artwork):
    id: PydanticObjectId = Field(alias="_id")
