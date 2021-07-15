from app.models.services_model import ServicesModel
from flask import Blueprint, json, jsonify,current_app, request
from flask_jwt_extended import (get_jwt_identity,
    jwt_required,
)

bp  = Blueprint("bp", __name__, url_prefix="/services")

@bp.get("/")
def get_services():
    try:
        
        services = ServicesModel.query.order_by(ServicesModel.name).all()
        services = [service.serialize for service in services]

        return jsonify(services)

    except:
        ...

@bp.post("/register")
@jwt_required()
def create_client():
    session = current_app.db.session
    try:
        data = request.get_json()

        service = ServicesModel(**data)

        session.add(service)
        session.commit()

        return {"message":"service created"}, 201

    except:
        ...

@bp.get("/<int:id>")
def get_service_by_id(id):
    current_service_id = get_jwt_identity()
    if current_service_id == id:
        try:
            service = ServicesModel.query.get(current_service_id)

            return jsonify(service.serialize)
        except:
            return {"message": "Not Found"}, 404
    return {"message": "unauthorized"}

# @bp.post("/<int:id>")
# @jwt_required()
# def create_service_by_id():
#     session = current_app.db.session
#     try:
#         data = request.get_json()

#         service = ServicesModel(**data)

#         session.add(service)
#         session.commit()

#         return {"message":"service created"}, 201

#     except:
#         ...

@bp.patch("/<int:id>")
@jwt_required()
def update_service_by_id(id):
    session = current_app.db.session
    current_service_id = get_jwt_identity()
    data = request.get_json()
    if current_service_id == id:
        try:
            service = ServicesModel.query.get(current_service_id)
            service.name = data["name"]
            session.commit()
            return jsonify(service.serialize)
        except KeyError:
            return {"message": "avaiable keys : name"}, 404
        except:
            return {"messege":"Not Found"}
    return {"message": "unauthorized"}


@bp.delete("/<int:id>")
@jwt_required()
def delete_service_by_id(id):
    current_service_id = get_jwt_identity()
    session = current_app.db.session
    if current_service_id == id:
        try:
            service = ServicesModel.query.get(current_service_id)
            session.delete(service)
            session.commit()
            return {"message":"deleted"}, 404
        except:
            return {"message":"Not Found"}, 404
    return {"message": "unauthorized"}