from fastapi import FastAPI
# from pydantic import BaseModel, Field
from .models import Artist
# from .models import Artwork

app = FastAPI()



@app.get("/")
def index():
    return {"message": "hola mundo"}

@app.get("/id/{id}")
def returnId(id: int):
    return {"id": id}

class Artist(BaseModel):
    id: int | None = Field(default=None)
    name: str
    pseudo: str
    description: str

@app.post("/artist")
def create_artist(artist:Artist):
    artista = artist
    return artista