__all__: list[str] = ["artwork_router"]

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic_mongo import PydanticObjectId

from ..models import Artwork, UpdateArtwork
from ..services import ArtworksServiceDependency, SecurityDependency
from ..__common_deps import QueryParamsDependency

artwork_router = APIRouter(prefix="/artworks", tags=["artworks"])


@artwork_router.get("/")
async def list_artworks(
    artworks: ArtworksServiceDependency, params: QueryParamsDependency
):
    return artworks.get_all(params)


@artwork_router.get("/{id}")
async def get_product(id: PydanticObjectId, artworks: ArtworksServiceDependency):
    return artworks.get_one(id) or JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Artwork with id: {id}, was not found."},
    )


@artwork_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_artwork(
    artwork: Artwork,
    artworks: ArtworksServiceDependency,
    security: SecurityDependency,
):
    security.is_artist_or_raise
    inserted_id = artworks.create_one(artwork)
    return {"result message": f"Artwork created with id: {inserted_id}"}


@artwork_router.put("/{id}")
async def update_artwork(
    id: PydanticObjectId, artwork: UpdateArtwork, artworks: ArtworksServiceDependency
):
    return artworks.update_one(id, artwork)
