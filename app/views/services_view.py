from http import HTTPStatus
from app.exc.status_option import InvalidKeysError
from app.models.services_model import ServicesModel
from flask import Blueprint, json, jsonify,current_app, request
from flask_jwt_extended import (get_jwt_identity,
    jwt_required,
)
from app.services.services_service import (get_services, create_service, get_service_by_id, update_service)

bp  = Blueprint("bp", __name__, url_prefix="/services")

@bp.get("/")
def get():
    try:
        return jsonify(data=services), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND

@bp.post("/register")
@jwt_required()
def create():
    try:
        data = request.get_json()
        service = create_service(data)
        return json(data=service.serialize), HTTPStatus.CREATED
    except InvalidKeysError as e:
        return jsonify(e.message), HTTPStatus.BAD_REQUEST

@bp.get("/<int:id>")
def retrieve_by_id(service_id):
    try:
        service = get_service_by_id(service_id)
        return json(data=service.serialize), HTTPStatus.OK
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND

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
