from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic_mongo import PydanticObjectId

from ..config import COLLECTIONS, db
from ..models import (
    CreationUser,
    CreationUserAdmin,
    CreationUserCustomer,
    CreationUserArtist,
    PrivateStoredUser,
    PublicStoredUser,
    CreateArtist,
    CreateUserArtistAndArtist,
)
from .artists import ArtistsServiceDependency
from ..__common_deps import QueryParamsDependency


class UsersService:
    assert (collection_name := "users") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def create_admin(
        cls,
        user: CreationUserAdmin,
        hash_password: str,
    ):
        try:
            existing_user = cls.get_one(username=user.username, email=user.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Admin already exists"
                )
        except HTTPException:
            pass

        user_dict = user.model_dump(exclude={"password"}, exclude_unset=True)
        user_dict.update({"hash_password": hash_password})
        insert_user = CreationUserAdmin.model_validate(user_dict).model_dump()

        result = cls.collection.insert_one(insert_user)
        if result:
            return str(result.inserted_id)
        return None

    @classmethod
    def create_customer(
        cls,
        user: CreationUser,
        hash_password: str,
    ):
        try:
            existing_user = cls.get_one(
                username=user.username,
                email=user.email,
            )
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="User already exists"
                )
        except HTTPException:
            pass

        user_dict = user.model_dump(exclude={"password"}, exclude_unset=True)
        user_dict.update({"hash_password": hash_password})
        insert_user = CreationUserCustomer.model_validate(user_dict).model_dump()

        result = cls.collection.insert_one(insert_user)
        if result:
            return str(result.inserted_id)
        return None

    @classmethod
    def create_artist(
        cls,
        artist: CreateUserArtistAndArtist,
        artists: ArtistsServiceDependency,
        hash_password: str,
    ):
        try:
            existing_user = cls.get_one(username=artist.username, email=artist.email)
            existing_artist = artists.get_one(name=artist.name, pseudo=artist.pseudo)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="User already exists"
                )
            if existing_artist:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, detail="Artist already exists"
                )
        except HTTPException:
            pass

        # user_dict = artist.model_dump()
        # user_dict.update(hash_password=hash_password)

        # insert_user = CreationUserArtist.model_validate(user_dict).model_dump()
        # result_user = cls.collection.insert_one(insert_user)

        assert (collection_artists := "artists") in COLLECTIONS
        artists_coll = db[collection_artists]

        artist_dict = artist.model_dump()
        artist_dict.update(user_id="66d32a13f2c56068349e1868", commision=15)
        insert_artist = CreateArtist.model_validate(artist_dict)
        print(insert_artist)
        result_artist = artists_coll.insert_one(insert_artist)

        # if result_user and result_artist:
        #     return {
        #         "user_id": result_user.inserted_id,
        #         "artist_id": result_artist.inserted_id,
        #     }
        # return None

    @classmethod
    def get_all(cls, params: QueryParamsDependency):
        return [
            PublicStoredUser.model_validate(user).model_dump()
            for user in params.query_collection(cls.collection)
        ]

    @classmethod
    def get_one(
        cls,
        *,
        id: PydanticObjectId | None = None,
        username: str | None = None,
        email: str | None = None,
        with_password: bool = False,
    ):
        if all(q is None for q in (id, username, email)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No id, username or email provided",
            )
        filter = {
            "$or": [
                {"_id": id},
                {"username": username},
                {"email": email},
            ]
        }

        if db_user := cls.collection.find_one(filter):
            return (
                PrivateStoredUser.model_validate(db_user).model_dump()
                if with_password
                else PublicStoredUser.model_validate(db_user).model_dump()
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    @classmethod
    def update_password(cls, id: PydanticObjectId, hash_password: str):
        document = cls.collection.find_one_and_update(
            {"_id": id},
            {"$set": {"hash_password": hash_password}},
            return_document=True,
        )
        if document:
            return PublicStoredUser.model_validate(document).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )


UsersServiceDependency = Annotated[UsersService, Depends()]
