from http import HTTPStatus
from app.exc.status_option import InvalidKeysError
from app.exc.status_not_found import NotFoundError
from app.exc.status_unauthorized import Unauthorized
from app.models.services_model import ServicesModel
from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.services.helpers import is_admin
from app.services.services_service import (delete_service, get_services, create_service, get_service_by_id, update_service)

bp  = Blueprint("bp", __name__, url_prefix="/api")

@bp.get("/services/")
def get():
    services = get_services()
    return jsonify({"data": services}), HTTPStatus.OK

@bp.post("/services/")
@jwt_required()
def create():
    try:
        is_admin(get_jwt())
        data = request.get_json()
        service = create_service(data)
        return jsonify(data=service.serialize), HTTPStatus.CREATED
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED

@bp.get("/services/<int:service_id>")
@jwt_required()
def retrieve_by_id(service_id: int):
    try:
        is_admin(get_jwt())
        service = get_service_by_id(service_id)
        return jsonify(data=service.serialize), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED

@bp.patch("/services/<int:service_id>")
@jwt_required()
def update_service_by_id(service_id: int):
    data = request.get_json()
    try:
        is_admin(get_jwt())
        service = update_service(data, service_id)
        return jsonify(data=service.serialize), HTTPStatus.OK
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND


@bp.delete("/services/<int:service_id>")
@jwt_required()
def delete_service_by_id(service_id: int):
    try:
        is_admin(get_jwt())
        return delete_service(service_id), HTTPStatus.NO_CONTENT
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED
