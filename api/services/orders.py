__all__ = ["OrdersServiceDependency", "OrdersService"]


from typing import Annotated

from fastapi import Depends, HTTPException, status
from pydantic_mongo import PydanticObjectId

from ..services import ArtworksService
from ..config import COLLECTIONS, db
from ..models import Order, StoredOrder, OrderItems


class OrdersService:
    assert (collection_name := "orders") in COLLECTIONS
    collection = db[collection_name]

    @classmethod
    def get_order_price(
        cls,
        order_items: OrderItems,
        artworks=ArtworksService,
    ):
        price: float = 0
        for item in order_items:
            artwork_price = artworks.get_one(
                PydanticObjectId(item.get("artwork_id"))
            ).get("price")
            price += artwork_price * item.get("quantity")
            print(item)
        return price

    @classmethod
    def create_one(cls, order: Order):
        print(order)
        order.update(
            price=cls.get_order_price(order.get("order_items")), status="pending"
        )
        result = cls.collection.insert_one(order)
        if result:
            return str(result.inserted_id)
        return None

    @classmethod
    def get_one(cls, id: PydanticObjectId):
        if db_order := cls.collection.find_one({"_id": id}):
            return StoredOrder.model_validate(db_order).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

    @classmethod
    def get_all_customer(cls, customer_id: PydanticObjectId):
        return [
            StoredOrder.model_validate(order).model_dump()
            for order in cls.collection.find(
                {"customer_id": PydanticObjectId(customer_id)}
            )
        ]

    @classmethod
    def cancel_order(cls, order_id: PydanticObjectId):
        document = cls.collection.find_one_and_update(
            {"_id": order_id}, {"$set": {"status": "cancelled"}}
        )

        if document:
            return StoredOrder.model_validate(document).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )

    @classmethod
    def pay_order(cls, order_id: PydanticObjectId):
        document = cls.collection.find_one_and_update(
            {"_id": order_id}, {"$set": {"status": "paid"}}
        )

        if document:
            return StoredOrder.model_validate(document).model_dump()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )


OrdersServiceDependency = Annotated[OrdersService, Depends(OrdersService)]
