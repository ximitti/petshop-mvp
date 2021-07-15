from http import HTTPStatus
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy.exc import IntegrityError


from app.exc.status_option import InvalidKeysError
from app.exc.status_not_found import NotFoundError
from app.services import (
    create_petshop,
    get_token,
    update_petshop,
    delete_petshop,
    get_petshop,
    get_petshop_by_id,
)

bp = Blueprint("bp_petshot", __name__, url_prefix="/api")


@bp.get("/petshop")
@jwt_required()
def get():
    pet_shop = get_petshop()
    return jsonify({"data": pet_shop}), HTTPStatus.OK


@bp.post("/petshop/register")
def register():
    data = request.get_json()
    try:
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
        access_token = get_token(data)
        return jsonify(data={"access_token": access_token}), HTTPStatus.OK
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except NotFoundError as e:
        return (jsonify(e.message), HTTPStatus.NOT_FOUND)


@bp.get("/petshop/<int:id>")
@jwt_required()
def get_by_id(id):
    try:
        pet_shop = get_petshop_by_id(id)
        return jsonify(data=pet_shop), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST


@bp.patch("/petshop")
@jwt_required()
def patch():
    try:
        data = request.get_json()
        email = get_jwt_identity()
        pet_shop = update_petshop(data, email)
        return jsonify(data=pet_shop), HTTPStatus.OK
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST


@bp.delete("/petshop")
@jwt_required()
def delete():
    return delete_petshop(), HTTPStatus.NO_CONTENT
