from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.models import OrderModel, OrderServicesModel, ServicesModel


bp = Blueprint("bp_order", __name__, url_prefix="/api")


@bp.post("/orders/")
@jwt_required()
def register() -> tuple:
    session = current_app.db.session

    data = request.get_json()
    order: OrderModel = OrderModel(**data)

    session.add(order)
    session.commit()

    return (
        jsonify(order=order.serialize),
        HTTPStatus.CREATED,
    )


@bp.get("/orders/")
@jwt_required()
def get() -> tuple:

    # TODO: trazer todos os serviços e montar a saida
    output: list = []
    # output: list = [order.serialize for order in orders]
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

    return (
        jsonify(orders=output),
        HTTPStatus.OK,
    )


@bp.get("/orders/<int:order_id>")
@jwt_required()
def get_by_id(order_id: int) -> tuple:

    # TODO: trazer todos os serviços relacionados à order
    order: OrderModel = OrderModel.query.get(order_id)

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

    return (
        jsonify(order=order_json),
        HTTPStatus.OK,
    )


@bp.patch("/orders/<int:order_id>")
@jwt_required()
def update(order_id: int):
    ...


@bp.delete("/orders/<int:order_id>")
@jwt_required()
def delete(order_id: int):
    ...
