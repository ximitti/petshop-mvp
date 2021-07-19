from app.models.order_model import OrderModel
from app.services.client_service import check_valid_keys
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
    valid_keys = ["name", "species", "size", "allergy", "breed", "fur", "photo_url", "client_id"]
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
        pets: PetModel =  PetModel.query.filter_by(client_id=client_id).all()
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
