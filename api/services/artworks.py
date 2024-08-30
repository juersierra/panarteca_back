__all__ = ["ArtworksServiceDependency", "ArtworksService"]


from typing import Annotated

from fastapi import Depends
from pydantic_mongo import PydanticObjectId

from ..__common_deps import QueryParamsDependency
from ..config import COLLECTIONS, db
from ..models import BaseArtwork, UpdateArtwork, StoredArtwork


class ArtworksService:
    assert (collection_name := "artworks") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def create_one(cls, artwork: BaseArtwork):
        result = cls.collection.insert_one(artwork)
        if result:
            return str(result.inserted_id)
        return None

    @classmethod
    def get_all(cls, params: QueryParamsDependency):
        return [
            StoredArtwork.model_validate(artwork).model_dump()
            for artwork in params.query_collection(cls.collection)
        ]

    @classmethod
    def get_one(cls, id: PydanticObjectId):
        if db_artwork := cls.collection.find_one({"_id": id}):
            return StoredArtwork.model_validate(db_artwork).model_dump()
        else:
            return None

    @classmethod
    def update_one(cls, id: PydanticObjectId, artwork: UpdateArtwork):
        return cls.collection.find_one_and_update(
            {"_id": id}, {"$set": artwork.model_dump()}, return_document=True
        )

    @classmethod
    def delete_one(cls, id: PydanticObjectId):
        return cls.collection.find_one_and_delete({"_id": id})


ArtworksServiceDependency = Annotated[ArtworksService, Depends(ArtworksService)]
