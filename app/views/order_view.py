from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from http import HTTPStatus

from app.models import OrderModel

from app.exc import InvalidKeysError, NotFoundError, MissingKeysError

from app.services import OrderServices


bp = Blueprint("bp_order", __name__, url_prefix="/api")


@bp.post("/orders/")
@jwt_required()
def register() -> tuple:

    try:
        order: OrderModel = OrderServices.create_order(request.get_json())

        return (
            jsonify(order=order.serialize),
            HTTPStatus.CREATED,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except MissingKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )


@bp.get("/orders/")
@jwt_required()
def get() -> tuple:

    orders: list[dict] = OrderServices.get_all_orders()

    return (
        jsonify(orders=orders),
        HTTPStatus.OK,
    )


@bp.get("/orders/<int:order_id>")
@jwt_required()
def get_by_id(order_id: int) -> tuple:

    try:
        order_json: dict = OrderServices.get_order_by_id(order_id)

        return (
            jsonify(order=order_json),
            HTTPStatus.OK,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
        )


@bp.patch("/orders/<int:order_id>")
@jwt_required()
def update(order_id: int) -> tuple:

    try:

        order_json: dict = OrderServices.update_order_by_id(request.get_json())

        return (
            jsonify(order=order_json),
            HTTPStatus.ACCEPTED,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
        )


@bp.delete("/orders/<int:order_id>")
@jwt_required()
def delete(order_id: int) -> tuple:

    try:
        OrderServices.delete_order_by_id(order_id)

        return (
            "",
            HTTPStatus.NO_CONTENT,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
        )
