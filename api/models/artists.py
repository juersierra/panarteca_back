from pydantic import BaseModel, Field

__all__ = ["Artist"]


class Artist(BaseModel):
    id: int | None = Field(default=None)
    name: str
    pseudo: str
    description: str
