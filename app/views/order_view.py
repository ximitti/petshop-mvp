from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.models import OrderModel


bp = Blueprint("bp_order", __name__, url_prefix="/api")


@bp.post("/orders")
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


@bp.get("/orders")
@jwt_required()
def get() -> tuple:

    # TODO: trazer todos os serviços e montar a saida
    orders: OrderModel = OrderModel.query.all()

    output: list = [order.serialize for order in orders]

    return (
        jsonify(orders=output),
        HTTPStatus.OK,
    )


@bp.get("/orders/<int:order_id>")
@jwt_required()
def get_by_id(order_id: int) -> tuple:

    # TODO: trazer todos os serviços relacionados à order
    order: OrderModel = OrderModel.query.get(order_id)

    return (
        jsonify(order=order.serialize),
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
