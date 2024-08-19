__all__ = ["ArtworkServiceDependency"]


from typing import Annotated

from fastapi import Depends
from pydantic_mongo import PydanticObjectId

from ..config import COLLECTIONS, db
from ..models import BaseArtwork, StoredArtwork

class ArtworksService:
  assert (collection_name := "artworks") in COLLECTIONS
  collection = db[collection_name]

  @classmethod
  def create_one(cls, artwork: BaseArtwork):
    result = cls.collection.insert_one(artwork.model_dump())
    if result:
      return str(result.inserted_id)
    return None
  
  @classmethod
  def get_all(cls):
    return [
      StoredArtwork.model_validate(artwork).model_dump()
      for artwork in cls.collection.find()
    ]
  
  @classmethod
  def get_one(cls, id: PydanticObjectId):
    if db_artwork := cls.collection.find_one({"_id": id}):
      return StoredArtwork.model_validate(db_artwork).model_dump()
    else:
      return None
    
  @classmethod
  def update_one(cls, id:PydanticObjectId, artwork: BaseArtwork):
    return cls.collection.find_one_and_update(
      {"_id": id},
      {"$set": artwork.model_dump()},
      return_document=True
    )
  
  @classmethod
  def delete_one(cls, id:PydanticObjectId):
    return cls.collection.find_one_and_delete({"_id":id})
  
ArtworkServiceDependency = Annotated[ArtworksService, Depends(ArtworksService)]