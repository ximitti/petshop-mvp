from typing import ValuesView
from flask import Blueprint, jsonify, current_app, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from http import HTTPStatus

from app.models import ClientModel
from app.models import AddressModel

from app.services.client_service import check_valid_keys

from sqlalchemy.exc import IntegrityError


bp  = Blueprint("bp_client", __name__, url_prefix="/api")


@bp.get("/clients")
def get_clients():
    try:

        clients = ClientModel.query.order_by(ClientModel.name).all()
        clients = [client.serialize for client in clients]

        return jsonify(clients)

    except:
        return "", HTTPStatus.NOT_FOUND


@bp.post("/clients/register")
def create_client():
    session = current_app.db.session
    try:
        data = request.get_json()

        valid_keys = ["name", "email", "password", "phone", "address"]
        for key, _ in data.items():
            check_valid_keys(data, valid_keys, key)


        password_to_hash = data.pop("password")

        client = ClientModel(**data)

        client.password = password_to_hash

        session.add(client)
        session.commit()

        return {"message":"user created"}, HTTPStatus.CREATED

    except IntegrityError as _:
        return {"error": "User already exists"}, HTTPStatus.NOT_ACCEPTABLE


@bp.post("/clients/login")
def login():
    data = request.get_json()
    try:
        client = ClientModel.query.filter_by(email=data["email"]).first()

        if client.check_password(data["password"]):

            access_token = create_access_token(identity=client.id)

            return jsonify(access_token)

        return jsonify({"message": "Bad email or password"}), HTTPStatus.BAD_REQUEST

    except:
        return jsonify({"message": "Bad email or password"}), HTTPStatus.BAD_REQUEST


@bp.get("/clients/<int:id>")
@jwt_required()
def get_client_by_id(id):
    current_user_id = get_jwt_identity()
    if current_user_id == id:
        try:
            client = ClientModel.query.get(current_user_id)

            return jsonify(client.serialize)
        except:
            return {"message": "Not Found"}, HTTPStatus.NOT_FOUND
    return {"message": "unauthorized"}, HTTPStatus.UNAUTHORIZED


@bp.patch("/clients/<int:id>")
@jwt_required()
def update_client_by_id(id):
    session = current_app.db.session
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if current_user_id == id:
    
        client = ClientModel.query.get(current_user_id)
        valid_keys = ["name", "email", "password", "phone", "address"]
        for key, value in data.items():
            check_valid_keys(data, valid_keys, key)
            if key == "password":
                client.password = value
            else:
                setattr(client, key, value)

        session.add(client)
        session.commit()

        return jsonify(client.serialize)
    return {"message": "unauthorized"}, HTTPStatus.UNAUTHORIZED


@bp.delete("/clients/<int:id>")
@jwt_required()
def delete_client_by_id(id):
    current_user_id = get_jwt_identity()
    session = current_app.db.session

    if current_user_id == id:
        try:
            client = ClientModel.query.get(current_user_id)

            session.delete(client)
            session.commit()

            return {"message":"deleted"}, HTTPStatus.NOT_FOUND
        except:
            return {"message":"Not Found"}, HTTPStatus.NOT_FOUND

    return {"message": "unauthorized"}, HTTPStatus.UNAUTHORIZED


@bp.post("/clients/<int:id>/address")
@jwt_required()
def create_address(id):
    session = current_app.db.session
    data = request.get_json()
    data["client_id"] = id
    current_user_id = get_jwt_identity()

    if current_user_id == id:

        valid_keys = ["zip_code", "neighborhood", "street", "number", "complement", "client_id"]
        for key, _ in data.items():
            check_valid_keys(data, valid_keys, key)
        try:
            address = AddressModel(**data)
            session.add(address)
            session.commit()
            print(address.serialize)
            return ("address.serialize"), HTTPStatus.CREATED
        except IntegrityError as _:
            return {"error": "already exists"}, HTTPStatus.NOT_ACCEPTABLE
    return {"message": "unauthorized"}, HTTPStatus.UNAUTHORIZED


@bp.get("/clients/<int:id>/address")
@jwt_required()
def get_address(id):
    current_user_id = get_jwt_identity()
    
    if current_user_id == id:
        addresses = AddressModel.query.filter_by(client_id=id).all()

        addresses = [address.serialize for address in addresses]
    

        return jsonify(addresses), HTTPStatus.OK
    return {"message": "unauthorized"}, HTTPStatus.UNAUTHORIZED

@bp.patch("/clients/<int:id>/address/<int:add_id>")
@jwt_required()
def update_address(id, add_id):
    session = current_app.db.session
    current_user_id = get_jwt_identity()
    data = request.get_json()

    if current_user_id == id:
        try:
            address = AddressModel.query.get(add_id)
            valid_keys = ["zip_code", "neighborhood", "street", "number", "complement", "client_id"]

            for key, value in data.items():
                check_valid_keys(data, valid_keys, key)
                setattr(address, key, value)

            session.add(address)
            session.commit()

            return jsonify(address.serialize)
        except IntegrityError as _:
            return {"error": "zip_code already exists"}, HTTPStatus.NOT_ACCEPTABLE

    return {"message": "unauthorized"}, HTTPStatus.UNAUTHORIZED

@bp.delete("/clients/<int:id>/address/<int:add_id>")
@jwt_required()
def delete_edit_address(id, add_id):
    session = current_app.db.session
    current_user_id = get_jwt_identity()

    if current_user_id == id:
        address = AddressModel.query.get(add_id)
        session.delete(address)
        session.commit()
        return {"message":"deleted"}, HTTPStatus.NOT_FOUND

    return {"message": "unauthorized"}, HTTPStatus.UNAUTHORIZED