from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import api_router, auth_router
from .api.config import allowed_origins


app = FastAPI()
app.include_router(auth_router)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "hola mundo"}


# @app.get("/id/{id}")
# def returnId(id: int):
#     return {"id": id}

# @app.post("/artist")
# def create_artist(artist:Artist):
#     artista = artist
#     return artista

# @app.post("/artwork")
# def create_artwork(artwork:Artwork):
#     artista = artwork
#     return artista
