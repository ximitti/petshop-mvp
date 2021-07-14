from flask.globals import request
from app.models.client_model import ClientModel
from flask import Blueprint, jsonify,current_app, request

bp  = Blueprint("bp", __name__, url_prefix="/clients")


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

        return {"message":"user created"}, 201
    except:
        ...
    
    

# @bp("/login")
# def login():
#     return "loga um usuario ai python"

# @bp("/logout")
# def logout():
#     return "desloga um usuario ai python"

# @bp("/<int:id>")
# def get_client_by_id():
#     return "pega um usuario ai python"

# @bp("/<int:id>/address")
# def get_create_address():
#     return "registra ou pega um endereço ai python"

# @bp("/<int:id>/address/<int:id>")
# def delete_edit_address():
#     return "deleta ou edita um endereço ai python"
