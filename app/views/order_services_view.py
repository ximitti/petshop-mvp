from flask import Blueprint, request, jsonify
from http import HTTPStatus

from app.services import OrderServiceServices


bp = Blueprint("bp_order_services", __name__, url_prefix="/api")


@bp.post("/order_services")
def register() -> tuple:
    data = request.get_json()

    for service in data.get("services"):
        OrderServiceServices.create_order_service(data.get("order"), service)

    return (
        jsonify(message="Order registered"),
        HTTPStatus.CREATED,
    )
