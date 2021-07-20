from app.exc.status_unauthorized import Unauthorized
from app.services.helpers import is_admin
from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from sqlalchemy.exc import IntegrityError


from app.exc.status_option import InvalidKeysError
from app.exc.status_not_found import NotFoundError
from app.services import (
    create_petshop,
    get_admin_token,
    update_petshop,
    delete_petshop,
    get_petshop,
    get_petshop_by_id,
)

bp = Blueprint("bp_petshop", __name__, url_prefix="/api")


@bp.get("/petshop")
@jwt_required()
def get():
    try:
        is_admin(get_jwt())
        pet_shop = get_petshop()
        return jsonify({"data": pet_shop}), HTTPStatus.OK
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED


@bp.post("/petshop/register")
def register():
    try:
        data = request.get_json()
        pet_shop = create_petshop(data)
        return jsonify({"data": pet_shop}), HTTPStatus.CREATED
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except IntegrityError as _:
        return jsonify(error="Petshop already exists"), HTTPStatus.BAD_REQUEST


@bp.post("/petshop/login")
def login():
    try:
        data = request.get_json()
        access_token = get_admin_token(data)
        return jsonify(data={"access_token": access_token}), HTTPStatus.OK
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except NotFoundError as e:
        return (jsonify(e.message), HTTPStatus.NOT_FOUND)


@bp.get("/petshop/<int:id>")
@jwt_required()
def get_by_id(id):
    try:
        is_admin(get_jwt())
        pet_shop = get_petshop_by_id(id)
        return jsonify(data=pet_shop), HTTPStatus.OK
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST


@bp.patch("/petshop")
@jwt_required()
def patch():
    try:
        is_admin(get_jwt())
        data = request.get_json()
        email = get_jwt_identity()
        pet_shop = update_petshop(data, email)
        return jsonify(data=pet_shop), HTTPStatus.OK
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST


@bp.delete("/petshop/<int:id>")
@jwt_required()
def delete(id):
    try:
        is_admin(get_jwt())
        return delete_petshop(id), HTTPStatus.NO_CONTENT
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
