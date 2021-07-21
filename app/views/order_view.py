from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.models import OrderModel, OrderServicesModel, ServicesModel

from app.exc import InvalidKeysError
from app.services import (
    create_order,
    get_all_orders,
    get_order_by_id,
    update_order_by_id,
    delete_order_by_id,
)
from app.services.helpers import add_commit, delete_commit


bp = Blueprint("bp_order", __name__, url_prefix="/api")


@bp.post("/orders/")
@jwt_required()
def register() -> tuple:

    try:
        order: OrderModel = create_order(request.get_json())

        return (
            jsonify(order=order.serialize),
            HTTPStatus.CREATED,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )


@bp.get("/orders/")
@jwt_required()
def get() -> tuple:

    orders: list[dict] = get_all_orders()

    return (
        jsonify(orders=orders),
        HTTPStatus.OK,
    )


@bp.get("/orders/<int:order_id>")
@jwt_required()
def get_by_id(order_id: int) -> tuple:

    order_json: dict = get_order_by_id(order_id)

    return (
        jsonify(order=order_json),
        HTTPStatus.OK,
    )


@bp.patch("/orders/<int:order_id>")
@jwt_required()
def update(order_id: int) -> tuple:

    try:

        order_json: dict = update_order_by_id(request.get_json())

        return (
            jsonify(order=order_json),
            HTTPStatus.ACCEPTED,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )


@bp.delete("/orders/<int:order_id>")
@jwt_required()
def delete(order_id: int) -> tuple:

    delete_order_by_id(order_id)

    return (
        "",
        HTTPStatus.NO_CONTENT,
    )
