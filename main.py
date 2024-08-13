from fastapi import FastAPI
from .models import *

app = FastAPI()

@app.get("/")
def index():
    return {"message": "hola mundo"}

@app.get("/id/{id}")
def returnId(id: int):
    return {"id": id}

@app.post("/artist")
def create_artist(artist:Artist):
    artista = artist
    return artista

@app.post("/artwork")
def create_artwork(artwork:Artwork):
    artista = artwork
    return artista