from app.exc.status_option import InvalidKeysError
from app.exc.status_unauthorized import Unauthorized
from app.exc.status_not_found import NotFoundError
from flask import Blueprint, jsonify, request
from flask_jwt_extended import  get_jwt_identity, jwt_required,get_jwt
from app.services.helpers import is_admin
from http import HTTPStatus

from app.services import ClientServices

from sqlalchemy.exc import IntegrityError


bp  = Blueprint("bp_client", __name__, url_prefix="/api")


@bp.get("/clients")
@jwt_required()
def get_clients():
    try:
        is_admin(get_jwt())
        return jsonify({"data":ClientServices.get_clients()}),HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED

@bp.post("/clients/register")
def create_client():
    try:
        data = request.get_json()
        return jsonify({"data":ClientServices.create_client(data).serialize}), HTTPStatus.CREATED
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST

@bp.post("/clients/login")
def login():
    try:
        data = request.get_json()
        return jsonify({"data":{"access":ClientServices.get_token(data)}}), HTTPStatus.OK
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST

@bp.get("/clients/<int:id>")
@jwt_required()
def get_client_by_id(id):
    current_user_id = get_jwt_identity()
    try:
        if current_user_id == id or is_admin(get_jwt()):
            return jsonify({"data":ClientServices.get_client_by_id(id)})
        else:
            raise Unauthorized
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED

@bp.patch("/clients/<int:id>")
@jwt_required()
def update_client_by_id(id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if current_user_id == id or is_admin(get_jwt()):
            return jsonify(ClientServices.update_client(data, id))
        else:
            raise Unauthorized
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED


@bp.delete("/clients/<int:id>")
@jwt_required()
def delete_client_by_id(id):
    try:
        current_user_id = get_jwt_identity()
        if current_user_id == id or is_admin(get_jwt()):
            return ClientServices.delete_client(id), HTTPStatus.NO_CONTENT
        else:
            raise Unauthorized
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED

@bp.post("/clients/<int:id>/address")
@jwt_required()
def create_address(id):
    try:
        data = request.get_json()
        data["client_id"] = id
        current_user_id = get_jwt_identity()
        if current_user_id == id:
            return jsonify(ClientServices.create_address(id, data).serialize), HTTPStatus.CREATED
    except IntegrityError as _:
            return {"error": "already exists"}, HTTPStatus.NOT_ACCEPTABLE  

@bp.get("/clients/<int:id>/address")
@jwt_required()
def get_address(id):
    try:
        current_user_id = get_jwt_identity()
        if current_user_id == id:
            return jsonify({"data":ClientServices.get_addresses(id)}), HTTPStatus.OK
    except IntegrityError as _:
        return {"error": "already exists"}, HTTPStatus.NOT_ACCEPTABLE        
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND

@bp.patch("/clients/<int:id>/address/<int:add_id>")
@jwt_required()
def update_address(id, add_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if current_user_id == id:
            return jsonify(ClientServices.updade_address_by_id(data, add_id).serialize), HTTPStatus.OK
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except IntegrityError as _:
        return {"error": "already exists"}, HTTPStatus.NOT_ACCEPTABLE
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND

@bp.delete("/clients/<int:id>/address/<int:add_id>")
@jwt_required()
def delete_edit_address(id, add_id):
    try:
        current_user_id = get_jwt_identity()
        if current_user_id == id:
            return jsonify(ClientServices.delete_address_by_id(add_id)), HTTPStatus.NO_CONTENT
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND