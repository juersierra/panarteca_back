from pydantic import BaseModel, Field

__all__ = ["Artwork"]


class Artwork(BaseModel):

    id: int | None = Field(default=None)
    # De esta forma podemos hacer que el campo sea opcional para el momento de la
    # creacion en nuestro caso
    name: str
    description: str
    technique: str
    year: int
    price: float
