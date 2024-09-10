__all__ = ["Order", "Item", "OrderItems", "StoredOrder"]

from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from pydantic_mongo import PydanticObjectId


class Status(str, Enum):
    pending = "pending"
    paid = "paid"
    cancelled = "cancelled"


class Item(BaseModel):
    artwork_id: str
    quantity: int


class OrderItems(BaseModel):
    order_items: List[Item]


class Order(OrderItems):
    customer_id: PydanticObjectId
    price: float
    status: Status = Status.pending


class StoredOrder(Order):
    id: PydanticObjectId = Field(alias="_id")
