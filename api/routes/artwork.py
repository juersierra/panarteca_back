__all__: list[str] = ["artwork_router"]

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic_mongo import PydanticObjectId

from ..models import BaseArtwork, UpdateArtwork
from ..services import (
    ArtworksServiceDependency,
    SecurityDependency,
    ArtistsServiceDependency,
)
from ..__common_deps import QueryParamsDependency

artwork_router = APIRouter(prefix="/artworks", tags=["Artworks"])


@artwork_router.get("/")
async def list_artworks(
    artworks: ArtworksServiceDependency, params: QueryParamsDependency
):
    return artworks.get_all(params)


@artwork_router.get("/{id}")
async def get_artwork(id: PydanticObjectId, artworks: ArtworksServiceDependency):
    return artworks.get_one(id) or JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Artwork with id: {id}, was not found."},
    )


@artwork_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_artwork(
    artwork: BaseArtwork,
    artworks: ArtworksServiceDependency,
    artists: ArtistsServiceDependency,
    security: SecurityDependency,
):
    security.is_artist_or_raise
    insert_artwork = artwork.model_dump()
    insert_artwork.update(
        artist_id=PydanticObjectId(
            artists.get_one(user_id=PydanticObjectId(security.auth_user_id)).get("id")
        )
    )
    inserted_id = artworks.create_one(insert_artwork)
    return {"result message": f"Artwork created with id: {inserted_id}"}


@artwork_router.put("/{id}")
async def update_artwork(
    id: PydanticObjectId, artwork: UpdateArtwork, artworks: ArtworksServiceDependency
):
    return artworks.update_one(id, artwork)
