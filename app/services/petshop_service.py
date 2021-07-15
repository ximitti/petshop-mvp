from flask import current_app
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

    session = current_app.db.session
    pet_shop = PetshopModel(**data)
    session.add(pet_shop)
    session.commit()
    return pet_shop


def get_petshop():
    return PetshopModel.query.all()


def get_petshop_by_id(id):
    return PetshopModel.query.get(id)


def get_token(data):
    valid_keys = ["email", "password"]

    for key, _ in data.items():
        check_valid_keys(data, valid_keys, key)

    user = PetshopModel.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return None

    return create_access_token(identity=data["email"])


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

    return pet_shop


def check_valid_keys(data, valid_keys, key):
    if key not in valid_keys:
        raise InvalidKeysError(data, valid_keys)


def delete_petshop():
    session = current_app.db.session
    email = get_jwt_identity()

    pet_shop = PetshopModel.query.filter_by(email=email).first()

    session.delete(pet_shop)
    session.commit()

    return ""
