from fastapi import APIRouter

from ..models import CreationUser, CreateUserArtistAndArtist
from ..services import (
    UsersServiceDependency,
    AuthServiceDependency,
    ArtistsServiceDependency,
)


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/create_admin")
def create_admin(
    user: CreationUser, users: UsersServiceDependency, auth: AuthServiceDependency
):
    hash_password = auth.get_password_hash(user.password)
    inserted_id = users.create_admin(user, hash_password)
    return {"result message": f"Admin created with id: {inserted_id}"}


@users_router.post("/create_artist")
def create_artist(
    artist: CreateUserArtistAndArtist,
    users: UsersServiceDependency,
    artists: ArtistsServiceDependency,
    auth: AuthServiceDependency,
):
    hash_password = auth.get_password_hash(artist.password)
    inserted_id = users.create_artist(artist, artists, hash_password)
    return {"result message": f"Artist created with id: {inserted_id}"}


@users_router.post("/create_customer")
def create_customer(
    customer: CreationUser,
    users: UsersServiceDependency,
    auth: AuthServiceDependency,
):
    hash_password = auth.get_password_hash(customer.password)
    inserted_id = users.create_customer(customer, hash_password)
    return {"result message": f"Customer created with id: {inserted_id}"}
