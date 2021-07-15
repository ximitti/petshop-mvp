from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)


from app.exc.status_option import InvalidKeysError
from app.services import (
    create_petshop,
    get_token,
    update_petshop,
    delete_petshop,
    get_petshop,
    get_petshop_by_id,
)

bp = Blueprint("bp_petshot", __name__, url_prefix="/api")


@bp.route("/petshop")
@jwt_required()
def get():
    return get_petshop()


@bp.route("/petshop/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        return create_petshop(data)
    except InvalidKeysError as e:
        return e.message


@bp.route("/petshop/login", methods=["POST"])
def login():
    data = request.get_json()
    try:
        return get_token(data)
    except InvalidKeysError as e:
        return e.message


@bp.route("/petshop/<int:id>")
@jwt_required()
def get_by_id(id):
    return get_petshop_by_id(id)


@bp.route("/petshop", methods=["PATCH"])
@jwt_required()
def patch():
    data = request.get_json()
    email = get_jwt_identity()
    try:
        return update_petshop(data, email)
    except InvalidKeysError as e:
        return e.message


@bp.route("/petshop", methods=["DELETE"])
@jwt_required()
def delete():
    return delete_petshop()
