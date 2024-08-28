__all__ = ["Order", "StoredOrder"]

from enum import Enum
from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId


class Status(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class Order(BaseModel):
    customer_id: PydanticObjectId
    artwork_id: PydanticObjectId
    price: float
    status: Status


class StoredOrder(Order):
    id: PydanticObjectId = Field(alias="_id")
