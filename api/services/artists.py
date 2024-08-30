__all__ = ["ArtistsService", "ArtistsServiceDependency"]

from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic_mongo import PydanticObjectId

from ..models import (
    PublicStoredArtist,
    PublicUpdateArtist,
)

from ..config import COLLECTIONS, db

from ..__common_deps import QueryParamsDependency


class ArtistsService:
    assert (collection_name := "artists") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def get_all(cls):
        return [
            PublicStoredArtist.model_validate(artist).model_dump()
            for artist in cls.collection.find()
        ]

    @classmethod
    def get_one(
        cls,
        *,
        id: PydanticObjectId | None = None,
        name: str | None = None,
        pseudo: str | None = None,
        user_id: PydanticObjectId | None = None,
    ):
        if all(q is None for q in (id, name, pseudo, user_id)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No filter provided",
            )
        filter = {
            "$or": [
                {"_id": id},
                {"name": name},
                {"pseudo": pseudo},
                {"user_id": user_id},
            ]
        }

        if db_user := cls.collection.find_one(filter):
            return PublicStoredArtist.model_validate(db_user).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

    @classmethod
    def update_one(cls, id: PydanticObjectId, artist: PublicUpdateArtist):
        document = cls.collection.find_one_and_update(
            {"_id": id}, {"$set": artist.model_dump()}, return_document=True
        )

        if document:
            return PublicStoredArtist.model_validate(document).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Artist not found"
            )


ArtistsServiceDependency = Annotated[ArtistsService, Depends()]
