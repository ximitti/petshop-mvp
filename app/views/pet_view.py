from app.models.pet_model import PetModel
from app.models.order_model import OrderModel
from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from http import HTTPStatus

bp = Blueprint("bp_pet", __name__, url_prefix="/api")


@bp.post('/pets/')
@jwt_required()
def create():
    session = current_app.db.session
    data = request.get_json()
    client_id = data['client_id']
    pet_owner_id = get_jwt_identity()

    try:   
        if client_id == pet_owner_id:
            pet: PetModel = PetModel(**data)
            session.add(pet)
            session.commit()
            return {"message": "Pet created", "data": pet.serialize}, HTTPStatus.CREATED
        else:
            raise KeyError  
    except KeyError as _:
        return {"error": "Unauthorized"}, HTTPStatus.UNAUTHORIZED

@bp.get('/pets/')
@jwt_required()
def retrieve_all():
    client_id = request.args.get('client_id')

    try:
        if client_id:
            pets: PetModel = PetModel.query.filter_by(client_id=client_id).all()
        else:
            pets: PetModel = PetModel.query.all()
    except:
        return {"error": "Internal Error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    pets = [pet.serialize for pet in pets]
    return {
        "data": pets
    }, HTTPStatus.OK

@bp.get('/pets/<int:pet_id>')
@jwt_required()
def retrieve_by_id(pet_id: int):
    try:
        pet: PetModel = PetModel.query.get(pet_id)

        if not pet:
            raise KeyError
        else:
            return {"data": pet.serialize}, HTTPStatus.OK
    except KeyError as _:
        return {"error": "Pet not found"}, HTTPStatus.NOT_FOUND


@bp.patch('/pets/<int:pet_id>')
@jwt_required()
def update(pet_id: int):
    session = current_app.db.session
    data = request.get_json()

    try:
        pet: PetModel = PetModel.query.get(pet_id)
        pet.name = data["name"]
        session.commit()
        return {"data": pet.serialize}, HTTPStatus.OK
    except KeyError:
        return {"error": "Internal Error"}, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.delete('/pets/<int:pet_id>')
@jwt_required()
def delete(pet_id: int):
    session = current_app.db.session
    current_user_id = get_jwt_identity()

    try:
        pet: PetModel = PetModel.query.get(pet_id)

        if pet.client_id == current_user_id:
            session.delete(pet)
            session.commit()
            return {"message": "Successful delete"}, HTTPStatus.NO_CONTENT
        else:
            raise KeyError

    except KeyError as _:
        return {"error": "Unauthorized"}, HTTPStatus.UNAUTHORIZED


@bp.get('/pets/<int:pet_id>/orders')
@jwt_required()
def get_orders_by_pet(pet_id: int):
    pet_owner_id = get_jwt_identity()

    try:
        pet: PetModel = PetModel.query.get(pet_id)
        if not pet:
            raise KeyError

        if pet.client_id == pet_owner_id:
            orders: OrderModel = OrderModel.query.filter_by(pet_id=pet_id).all()
            orders = [order.serialize for order in orders]
            return {"data": orders}, HTTPStatus.OK
        else:
            return {"error": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
    except KeyError as _:
        return {"error": "Pet not found"}, HTTPStatus.NOT_FOUND