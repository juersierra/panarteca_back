from fastapi import APIRouter

from ..models import CreationUserAdmin, CreateUserArtistAndArtist
from ..services import UsersServiceDependency, AuthServiceDependency


users_router = APIRouter(prefix="/users", tags=["Auth"])


@users_router.post("/create_admin")
def create_admin(
    user: CreationUserAdmin, users: UsersServiceDependency, auth: AuthServiceDependency
):
    hash_password = auth.get_password_hash(user.password)
    inserted_id = users.create_admin(user, hash_password)
    return {"result message": f"Admin created with id: {inserted_id}"}


@users_router.post("/create_artist")
def create_artist(
    artist: CreateUserArtistAndArtist,
    users: UsersServiceDependency,
    auth: AuthServiceDependency,
):
    hash_password = auth.get_password_hash(artist.password)
    inserted_id = users.create_artist(artist, hash_password)
    return {"result message": f"Artist created with id: {inserted_id}"}
