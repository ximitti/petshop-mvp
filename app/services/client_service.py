from flask import current_app, jsonify
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.exc.status_option import InvalidKeysError
from app.models import ClientModel
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
)

def get_clients():
    client = ClientModel.query.all()
    return jsonify(client), HTTPStatus.OK

def create_client(data):
    valid_keys = ["name", "email", "password", "phone", "address"]
    for key, _ in data.items():
        check_valid_keys(data, valid_keys, key)
    try:
        session = current_app.db.session
        password_to_hash = data.pop("password")
        client = ClientModel(**data)
        client.password = password_to_hash
        session.add(client)
        session.commit()

        return {"message":"user created"}, HTTPStatus.CREATED

    except IntegrityError as _:
        return {"error": "Petshop already exists"}, HTTPStatus.NOT_ACCEPTABLE


def get_token(data):
    valid_keys = ["email", "password"]
    for key, _ in data.items():
        check_valid_keys(data, valid_keys, key)
    client = ClientModel.query.filter_by(email=data["email"]).first()

    if not client or not client.check_password(data["password"]):
        return (
            jsonify({"msg": "Bad username or password"}),
            HTTPStatus.NOT_FOUND,
        )

    access_token = create_access_token(identity=client.id)

    return jsonify(access_token=access_token), HTTPStatus.OK

def get_client_by_id(id):
    client = ClientModel.query.get(id)
    if not client:
        return {"error": "Not Found"}, HTTPStatus.NOT_FOUND
    return jsonify(client), HTTPStatus.OK


def update_client(data, id):
    valid_keys = ["name", "email", "password", "phone"]
    session = current_app.db.session
    client = ClientModel.query.get(id)

    for key, value in data.items():

        check_valid_keys(data, valid_keys, key)

        if key == "password":
            client.password = value
        else:
            setattr(client, key, value)

    session.add(client)
    session.commit()

    return jsonify(client), HTTPStatus.OK

def delete_client(id):
    session = current_app.db.session
    client = ClientModel.query.get(id)

    session.delete(client)
    session.commit()

    return "", HTTPStatus.NO_CONTENT



def check_valid_keys(data, valid_keys, key):
    if key not in valid_keys:
        raise InvalidKeysError(data, valid_keys)