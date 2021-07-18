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