from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus

from app.models import OrderServicesModel


bp = Blueprint("bp_order_services", __name__, url_prefix="/api")


@bp.post("/order_services")
def register():
    session = current_app.db.session

    data = request.get_json()

    for service in data.get("services"):
        print(service)

        order_service: OrderServicesModel = OrderServicesModel(
            order_id=data.get("order"), services_id=service
        )

        session.add(order_service)
        session.commit()

    # order_service = OrderServicesModel(**data)

    # return jsonify(data=order_service), HTTPStatus.CREATED
    return "<h1>Order Service</h1>"
