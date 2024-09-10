__all__: list[str] = ["order_router"]

from typing import List
from fastapi import status
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from pydantic_mongo import PydanticObjectId

from ..services import (
    OrdersServiceDependency,
    SecurityDependency,
    ArtworksServiceDependency,
)
from ..models import Order, StoredOrder, Item, OrderItems

order_router = APIRouter(prefix="/orders", tags=["Orders"])


@order_router.get("/")
async def get_customer_orders(
    orders: OrdersServiceDependency,
    security: SecurityDependency,
):
    security.is_customer_or_raise
    print(security.auth_user_id)
    return orders.get_all_customer(security.auth_user_id)


@order_router.get("/{id}/")
async def get_order(id: PydanticObjectId, orders: OrdersServiceDependency):
    return orders.get_one(id) or JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"error": f"Artwork with id: {id}, was not found."},
    )


@order_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    orderItems: OrderItems,
    orders: OrdersServiceDependency,
    security: SecurityDependency,
):
    security.is_customer_or_raise

    insert_order = dict(
        order_items=orderItems.model_dump().get("order_items"),
        customer_id=PydanticObjectId(security.auth_user_id),
    )
    inserted_id = orders.create_one(insert_order)
    return inserted_id


@order_router.post("/{id}/pay/")
async def pay_order(id: PydanticObjectId, orders: OrdersServiceDependency):
    orders.pay_order(id)
    return {"result message": f"order {id} paid successfully"}


@order_router.post("/{id}/cancel/")
async def cancel_order(id: PydanticObjectId, orders: OrdersServiceDependency):
    orders.cancel_order(id)
    return {"result message": f"order {id} cancelled successfully"}
