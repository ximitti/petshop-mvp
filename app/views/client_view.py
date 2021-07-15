from flask import Blueprint, json, jsonify, current_app, request
from http import HTTPStatus

from app.models import ClientModel

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


bp = Blueprint("bp", __name__, url_prefix="/clients")


@bp.get("/")
def get_clients():
    try:

        clients = ClientModel.query.order_by(ClientModel.name).all()
        clients = [client.serialize for client in clients]

        return jsonify(clients)

    except:
        ...


@bp.post("/register")
def create_client():
    session = current_app.db.session
    try:
        data = request.get_json()

        password_to_hash = data.pop("password")

        client = ClientModel(**data)

        client.password = password_to_hash

        session.add(client)
        session.commit()

        return {"message": "user created"}, 201

    except:

        return {"error":"User already exists"}, HTTPStatus.BAD_REQUEST


@bp.post("/login")
def login():
    data = request.get_json()
    try:
        client = ClientModel.query.filter_by(email=data["email"]).first()

        if client.check_password(data["password"]):

            access_token = create_access_token(identity=client.id)

            return jsonify(access_token)

        return jsonify({"message": "Bad email or password"}), 401

    except:
        return jsonify({"message": "Bad email or password"}), 401


@bp.get("/<int:id>")
@jwt_required()
def get_client_by_id(id):
    current_user_id = get_jwt_identity()
    if current_user_id == id:
        try:
            client = ClientModel.query.get(current_user_id)

            return jsonify(client.serialize)
        except:
            return {"message": "Not Found"}, 404
    return {"message": "unauthorized"}


@bp.patch("/<int:id>")
@jwt_required()
def update_client_by_id(id):
    session = current_app.db.session
    current_user_id = get_jwt_identity()
    data = request.get_json()
    if current_user_id == id:
        try:
            client = ClientModel.query.get(current_user_id)
            client.name = data["name"]
            session.commit()
            return jsonify(client.serialize)
        except KeyError:
            return {"message": "avaiable keys : name"}, 404
        except:
            return {"messege": "Not Found"}
    return {"message": "unauthorized"}


@bp.delete("/<int:id>")
@jwt_required()
def delete_client_by_id(id):
    current_user_id = get_jwt_identity()
    session = current_app.db.session
    if current_user_id == id:
        try:
            client = ClientModel.query.get(current_user_id)
            session.delete(client)
            session.commit()
            return {"message": "deleted"}, 404
        except:
            return {"message": "Not Found"}, 404
    return {"message": "unauthorized"}


# @bp("/<int:id>/address")
# def get_create_address():
#     return "registra ou pega um endereço ai python"

# @bp("/<int:id>/address/<int:id>")
# def delete_edit_address():
#     return "deleta ou edita um endereço ai python"
