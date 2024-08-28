__all__ = ["Artwork", "UpdateArtwork", "SellArtwork", "StoredArtwork"]

from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId


class Artwork(BaseModel):
    name: str
    description: str
    technique: str
    year: int
    price: float
    serie: str
    artist_id: PydanticObjectId
    collection_id: PydanticObjectId = Field(default=None)
    sold: bool = False


class UpdateArtwork(BaseModel):
    name: str = Field(default=None)
    description: str = Field(default=None)
    technique: str = Field(default=None)
    year: int = Field(default=None)
    price: float = Field(default=None)
    serie: str = Field(default=None)
    artist_id: PydanticObjectId = Field(default=None)
    collection_id: PydanticObjectId = Field(default=None)


class SellArtwork(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    sold: bool = True


class StoredArtwork(Artwork):
    id: PydanticObjectId = Field(alias="_id")
