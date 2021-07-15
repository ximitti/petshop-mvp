from flask import current_app, jsonify
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.exc.status_option import InvalidKeysError
from app.models import PetshopModel
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
)


def create_petshop(data):
    valid_keys = ["name", "email", "password", "is_admin"]
    for key, _ in data.items():
        check_valid_keys(data, valid_keys, key)

    try:
        session = current_app.db.session
        pet_shop = PetshopModel(**data)
        session.add(pet_shop)
        session.commit()
        return jsonify(pet_shop), HTTPStatus.CREATED
    except IntegrityError as _:
        return {"error": "Petshop already exists"}, HTTPStatus.NOT_ACCEPTABLE


def get_petshop():
    pet_shop = PetshopModel.query.all()
    return jsonify(pet_shop), HTTPStatus.OK


def get_petshop_by_id(id):
    pet_shop = PetshopModel.query.get(id)
    if not pet_shop:
        return {"msg": "Petshop not found"}
    return jsonify(pet_shop), HTTPStatus.OK


def get_token(data):
    valid_keys = ["email", "password"]
    for key, _ in data.items():
        check_valid_keys(data, valid_keys, key)

    user = PetshopModel.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return (
            jsonify({"msg": "Bad username or password"}),
            HTTPStatus.NOT_FOUND,
        )

    access_token = create_access_token(identity=data["email"])
    return jsonify(access_token=access_token), HTTPStatus.OK


def update_petshop(data, email):
    valid_keys = ["name", "email", "password", "is_admin"]
    session = current_app.db.session
    pet_shop = PetshopModel.query.filter_by(email=email).first()

    for key, value in data.items():

        check_valid_keys(data, valid_keys, key)

        if key == "password":
            pet_shop.password = value
        else:
            setattr(pet_shop, key, value)

    session.add(pet_shop)
    session.commit()

    return jsonify(pet_shop), HTTPStatus.OK


def check_valid_keys(data, valid_keys, key):
    if key not in valid_keys:
        raise InvalidKeysError(data, valid_keys)


def delete_petshop():
    session = current_app.db.session
    email = get_jwt_identity()

    pet_shop = PetshopModel.query.filter_by(email=email).first()

    session.delete(pet_shop)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
