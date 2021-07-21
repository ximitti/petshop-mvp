from app.models import OrderModel, OrderServicesModel, ServicesModel


from app.exc import InvalidKeysError
from app.services.helpers import add_commit, delete_commit, check_valid_keys


def create_order(data: dict) -> OrderModel:
    valid_keys = ["date", "finished_date", "pet_delivery", "pet_id"]

    if check_valid_keys(data, valid_keys):
        raise InvalidKeysError(data, valid_keys)

    order: OrderModel = OrderModel(**data)

    add_commit(order)

    return order


def update_order_by_id(id: int, data: dict) -> dict:
    valid_keys = ["finished_date", "pet_delivery"]

    if check_valid_keys(data, valid_keys):
        raise InvalidKeysError(data, valid_keys)

    order: OrderModel = OrderModel.query.get(id)

    for key, value in data.items():
        setattr(order, key, value)

    add_commit(order)

    return order.serialize


def delete_order_by_id(id: int) -> None:

    order: OrderModel = OrderModel.query.get(id)

    delete_commit(order)


def get_all_orders() -> list[dict]:
    output: list = []

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
            {"id": item[0], "name": item[1], "description": item[2], "price": item[3]}
            for item in query
        ]

        output.append(order_json)

    return output


def get_order_by_id(id: int) -> dict:
    order: OrderModel = OrderModel.query.get(id)

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
