from flask import Blueprint, request, current_app, jsonify
from http import HTTPStatus
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy.exc import IntegrityError
from app.models import PetshopModel
from app.services import create_petshop

bp = Blueprint("bp_petshot", __name__, url_prefix="/api")


@bp.route("/petshop")
@jwt_required()
def get():
    pet_shop = PetshopModel.query.all()
    return jsonify(pet_shop)


@bp.route("/petshop/register", methods=["POST"])
def register():
    data = request.get_json()
    try:
        return create_petshop(data)
    except IntegrityError as _:
        return {"error": "Petshop already exists"}


@bp.route("/petshop/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = PetshopModel.query.filter_by(email=email).first()
    user.check_password(password)

    if not user or not user.check_password(password):
        return (
            jsonify({"msg": "Bad username or password"}),
            HTTPStatus.NOT_FOUND,
        )

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


@bp.route("/petshop/logout", methods=["POST"])
@jwt_required()
def logout():
    pass


@bp.route("/petshop/<int:id>")
@jwt_required()
def get_by_id(id):
    pet_shop = PetshopModel.query.get(id)
    return jsonify(pet_shop)


@bp.route("/petshop", methods=["PATCH"])
@jwt_required()
def patch():
    session = current_app.db.session
    data = request.get_json()
    email = get_jwt_identity()

    pet_shop = PetshopModel.query.filter_by(email=email).first()

    for key, value in data.items():

        setattr(pet_shop, key, value)

    session.add(pet_shop)
    session.commit()

    return pet_shop.serialize, HTTPStatus.OK


@bp.route("/petshop", methods=["DELETE"])
@jwt_required()
def delete():
    session = current_app.db.session
    email = get_jwt_identity()

    pet_shop = PetshopModel.query.filter_by(email=email).first()

    session.delete(pet_shop)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
