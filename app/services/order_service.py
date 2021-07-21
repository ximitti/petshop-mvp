from app.models import OrderModel, OrderServicesModel, ServicesModel

from app.exc import InvalidKeysError, NotFoundError, MissingKeysError
from app.services.helpers import (
    add_commit,
    delete_commit,
    check_valid_keys,
    check_missed_keys,
)


class OrderServices:
    @staticmethod
    def create_order(data: dict) -> OrderModel:
        valid_keys = ["date", "finished_date", "pet_delivery", "pet_id"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        required_fields = ["date", "pet_id"]
        missed_fields: list[str] = check_missed_keys(data, required_fields)
        if missed_fields:
            raise MissingKeysError(required_fields, missed_fields)

        order: OrderModel = OrderModel(**data)

        add_commit(order)

        return order

    @staticmethod
    def update_order_by_id(id: int, data: dict) -> dict:
        valid_keys = ["finished_date", "pet_delivery"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        order: OrderModel = OrderModel.query.get(id)
        if not order:
            raise NotFoundError("Order not found")

        for key, value in data.items():
            setattr(order, key, value)

        add_commit(order)

        return order.serialize

    @staticmethod
    def delete_order_by_id(id: int) -> None:

        order: OrderModel = OrderModel.query.get(id)
        if not order:
            raise NotFoundError("Order not found")

        delete_commit(order)

    @staticmethod
    def get_all_orders() -> list[dict]:
        orders_json: list[dict] = []

        orders: OrderModel = OrderModel.query.all()

        for order in orders:

            query = (
                OrderModel.query.from_self(
                    ServicesModel.id,
                    ServicesModel.name,
                    ServicesModel.description,
                    ServicesModel.price,
                )
                .join(OrderServicesModel)
                .join(ServicesModel)
                .filter(OrderModel.id == order.id)
                .all()
            )

            order_json = order.serialize
            order_json["services"] = [
                {
                    "id": item[0],
                    "name": item[1],
                    "description": item[2],
                    "price": item[3],
                }
                for item in query
            ]

            orders_json.append(order_json)

        return orders_json

    @staticmethod
    def get_order_by_id(id: int) -> dict:
        order: OrderModel = OrderModel.query.get(id)
        if not order:
            raise NotFoundError("Order not found")

        query = (
            OrderModel.query.from_self(
                ServicesModel.id,
                ServicesModel.name,
                ServicesModel.description,
                ServicesModel.price,
            )
            .join(OrderServicesModel)
            .join(ServicesModel)
            .filter(OrderModel.id == order.id)
            .all()
        )

        order_json = order.serialize
        order_json["services"] = [
            {"id": item[0], "name": item[1], "description": item[2], "price": item[3]}
            for item in query
        ]

        return order_json
