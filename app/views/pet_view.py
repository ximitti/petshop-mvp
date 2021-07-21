from app.exc.status_unauthorized import Unauthorized
from app.services.pet_service import delete_pet, get_pet_orders, update_pet
from app.exc.status_option import InvalidKeysError
from app.exc.status_not_found import NotFoundError
from app.models.pet_model import PetModel
from app.models.order_model import OrderModel
from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

from app.services import (
    create_pet,
    get_pets,
    get_pet_by_id
)

bp = Blueprint("bp_pet", __name__, url_prefix="/api")


@bp.post('/pets/')
@jwt_required()
def create():
    try:   
        data = request.get_json()
        pet_owner_id = get_jwt_identity()
        client_id = data['client_id']
        if client_id == pet_owner_id:
            pet = create_pet(client_id, pet_owner_id, data)
            return jsonify(data=pet.serialize), HTTPStatus.CREATED
        else:
            raise Unauthorized
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED

@bp.get('/pets/')
@jwt_required()
def retrieve_all():
    try:
        client_id = request.args.get('client_id')
        pets = get_pets(client_id)
        return jsonify(data=pets), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND

@bp.get('/pets/<int:pet_id>')
@jwt_required()
def retrieve_by_id(pet_id: int):
    try:
        pet = get_pet_by_id(pet_id)
        return jsonify(data=pet.serialize), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND


@bp.patch('/pets/<int:pet_id>')
@jwt_required()
def update(pet_id: int):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        pet = update_pet(data, pet_id, current_user_id)
        return jsonify(data=pet.serialize), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED


@bp.delete('/pets/<int:pet_id>')
@jwt_required()
def delete(pet_id: int):
    try:
        current_user_id = get_jwt_identity()
        delete_pet(pet_id, current_user_id)
        return "", HTTPStatus.NO_CONTENT
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED


@bp.get('/pets/<int:pet_id>/orders')
@jwt_required()
def get_orders_by_pet(pet_id: int):
    try:
        pet_owner_id = get_jwt_identity()
        pet = get_pet_by_id(pet_id)
        if pet.client_id == pet_owner_id:
            orders = get_pet_orders(pet_id)
            return jsonify(data=orders), HTTPStatus.OK
        else:
            raise Unauthorized
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED