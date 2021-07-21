from http import HTTPStatus
from app.exc.status_option import InvalidKeysError
from app.exc.status_not_found import NotFoundError
from app.models.services_model import ServicesModel
from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from app.services.helpers import is_admin
from app.services.services_service import (delete_service, get_services, create_service, get_service_by_id, update_service)

bp  = Blueprint("bp", __name__, url_prefix="/services")

@bp.get("/")
def get():
    services = get_services()
    return jsonify({"data": services}), HTTPStatus.OK

@bp.post("/register")
@jwt_required()
def create():
    try:
        is_admin(get_jwt())
        data = request.get_json()
        service = create_service(data)
        return json(data=service.serialize), HTTPStatus.CREATED
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST

@bp.get("/<int:id>")
def retrieve_by_id(service_id):
    try:
        is_admin(get_jwt())
        service = get_service_by_id(service_id)
        return json(data=service.serialize), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND

@bp.patch("/<int:id>")
@jwt_required()
def update_service_by_id(service_id):
    data = request.get_json()
    try:
        is_admin(get_jwt())
        service = update_service(data, service_id)
        return jsonify(data=service), HTTPStatus.OK
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST


@bp.delete("/<int:id>")
@jwt_required()
def delete_service_by_id(id):
    try:
        is_admin(get_jwt())
        return delete_service(), HTTPStatus.NO_CONTENT
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
