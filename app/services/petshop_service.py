from app.exc.status_unauthorized import Unauthorized
from flask import current_app
from app.exc import InvalidKeysError, NotFoundError
from app.models import PetshopModel
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
)
import ipdb


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
    pet_shop = PetshopModel.query.get(id)
    if not pet_shop:
        raise NotFoundError("Petshop not found")
    return pet_shop


def get_admin_token(data):
    valid_keys = ["email", "password"]

    for key, _ in data.items():
        check_valid_keys(data, valid_keys, key)

    user = PetshopModel.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        raise NotFoundError("Bad username or password")

    return create_access_token(
        identity=data["email"], additional_claims={"is_admin": user.is_admin}
    )


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


def delete_petshop(id):
    session = current_app.db.session
    email = get_jwt_identity()

    pet_shop = PetshopModel.query.filter_by(email=email).first()
    pet_shop_to_be_deleted = PetshopModel.query.get(id)

    if not pet_shop_to_be_deleted:
        raise NotFoundError("User Petshop not found")

    if pet_shop.id == pet_shop_to_be_deleted.id:
        raise Unauthorized("You can't delete your own user")

    if pet_shop_to_be_deleted.is_admin:
        raise Unauthorized("You can't delete admin users")

    session.delete(pet_shop_to_be_deleted)
    session.commit()

    return ""
