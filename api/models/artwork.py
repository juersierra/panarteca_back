from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId

__all__ = ["BaseArtwork","StoredArtwork"]


class BaseArtwork(BaseModel):
    # De esta forma podemos hacer que el campo sea opcional para el momento de la
    # creacion en nuestro caso

    name: str
    description: str
    technique: str
    year: int
    price: float

class StoredArtwork(BaseArtwork):
    id: PydanticObjectId = Field(alias="_id")