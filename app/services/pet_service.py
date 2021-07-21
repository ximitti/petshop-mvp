from flask_jwt_extended.utils import get_jwt
from app.services.helpers import is_admin
from app.exc.status_unauthorized import Unauthorized
from app.models.order_model import OrderModel
from app.exc.status_not_found import NotFoundError
from app.models.pet_model import PetModel
from flask import current_app, jsonify
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.exc.status_option import InvalidKeysError
from app.models import PetshopModel
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
)


def check_valid_keys(data, valid_keys, key):
    if key not in valid_keys:
        raise InvalidKeysError(data, valid_keys)


def create_pet(client_id, pet_owner_id, data):
    valid_keys = [
        "name",
        "species",
        "size",
        "allergy",
        "breed",
        "fur",
        "photo_url",
        "client_id",
    ]
    for key, _ in data.items():
        check_valid_keys(data, valid_keys, key)

    session = current_app.db.session
    pet: PetModel = PetModel(**data)
    session.add(pet)
    session.commit()
    return pet


def get_pets(client_id: int):
    print(client_id)
    if client_id:
        pets: PetModel = PetModel.query.filter_by(client_id=client_id).all()
    else:
        pets: PetModel = PetModel.query.all()

    if not pets:
        raise NotFoundError("Pets not found")
    pets = [pet.serialize for pet in pets]
    return pets


def get_pet_by_id(pet_id: int):
    pet: PetModel = PetModel.query.get(pet_id)
    if not pet:
        raise NotFoundError("Pet not found")
    return pet


def get_pet_orders(pet_id: int):
    orders: OrderModel = OrderModel.query.filter_by(pet_id=pet_id).all()
    orders = [order.serialize for order in orders]
    return orders


def update_pet(data, pet_id: int, current_user_id: int):
    pet = get_pet_by_id(pet_id)
    session = current_app.db.session
    if pet.client_id == current_user_id or is_admin(get_jwt()):
        valid_keys = [
            "name",
            "species",
            "size",
            "allergy",
            "breed",
            "fur",
            "photo_url",
            "client_id",
        ]
        for key, value in data.items():
            check_valid_keys(data, valid_keys, key)

            setattr(pet, key, value)

        session.add(pet)
        session.commit()
        return pet
    else:
        raise Unauthorized


def delete_pet(pet_id: int, current_user_id: int) -> None:
    session = current_app.db.session
    pet = get_pet_by_id(pet_id)
    if pet.client_id == current_user_id or is_admin(get_jwt()):
        session.delete(pet)
        session.commit()
    else:
        raise Unauthorized
