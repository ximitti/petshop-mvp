from app.models.pet_model import PetModel
from flask import Blueprint, jsonify, current_app, request
# from flask_httpauth import HTTPTokenAuth
from http import HTTPStatus

bp = Blueprint("bp_pet", __name__, url_prefix="/pets")


@bp.post('')
def create():
    session = current_app.db.session
    data = request.get_json()

    try:
        pet: PetModel = PetModel(**data)
        session.add(pet)
        session.commit()
    except:
        return {"error": "Internal Error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {"message": "Pet created", "data": pet.serialize}, HTTPStatus.CREATED


@bp.get('')
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

@bp.get('/<int:pet_id>')
def retrieve_by_id(pet_id: int):
    try:
        pet: PetModel = PetModel.query.get(pet_id)
    except:
        return {"error": "Internal Error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    if not pet:
        return {"error": "Pet not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": pet}, HTTPStatus.OK

