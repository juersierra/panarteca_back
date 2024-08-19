__all__: list[str] = ["artwork_router"]

from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic_mongo import PydanticObjectId

from ..models import BaseArtwork
from ..services import ArtworkServiceDependency, AuthServiceDependency

artwork_router = APIRouter(prefix="/artworks", tags=["artworks"])


@artwork_router.get("/")
async def list_artworks(artworks: ArtworkServiceDependency):
    return artworks.get_all()


@artwork_router.get("/{id}")
async def get_artwork(id: PydanticObjectId, artworks: ArtworkServiceDependency):
    return artworks.get_one({"_id": id}) or JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Product with id: {id}, not found"},
    )


@artwork_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_artwork(
    artwork: BaseArtwork,
    artworks: ArtworkServiceDependency,
    auth: AuthServiceDependency,
):
    assert (
        auth.is_admin or auth.is_seller
    ), "Only admins and sellers can create artworks"
    inserted_id = artworks.create_one(artwork)
    return {"result message": f"Artwork created with id: {inserted_id}"}
