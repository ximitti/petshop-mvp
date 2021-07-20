from app.exc.status_unauthorized import Unauthorized
from http import HTTPStatus
from app.exc.status_not_found import NotFoundError
from app.services.helpers import is_admin
from flask_jwt_extended.utils import get_jwt
from app.models.services_model import ServicesModel
from flask import Blueprint, json, jsonify, current_app, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

bp = Blueprint("bp_service", __name__, url_prefix="/api")


@bp.get("/services/")
def get_services():
    try:

        services = ServicesModel.query.order_by(ServicesModel.name).all()
        services = [service.serialize for service in services]

        return jsonify(services)

    except:
        ...


@bp.post("/services/")
@jwt_required()
def register():
    session = current_app.db.session
    try:
        data = request.get_json()

        service = ServicesModel(**data)

        session.add(service)
        session.commit()

        return {"message": "service created"}, 201

    except:
        ...


@bp.get("/services/<int:id>")
@jwt_required()
def get_service_by_id(id):
    current_service_id = get_jwt_identity()
    try:
        service = ServicesModel.query.get(id)

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


@bp.patch("/services/<int:id>")
@jwt_required()
def update_service_by_id(id):
        try:
            session = current_app.db.session
            data = request.get_json()
            is_admin(get_jwt())
            service = ServicesModel.query.get(id)
            service.name = data["name"]
            session.add(service)
            session.commit()
            return jsonify(service.serialize)
        except KeyError:
            return {"message": "avaiable keys : name"}, 404
        except:
            return {"messege": "Not Found"},


@bp.delete("/services/<int:id>")
@jwt_required()
def delete_service_by_id(id):
    try:
        is_admin(get_jwt())
        session = current_app.db.session
        service = ServicesModel.query.get(id)
        if not service:
            raise NotFoundError("Service not found")
        session.delete(service)
        session.commit()
        return "", HTTPStatus.NO_CONTENT
    except NotFoundError as e:
        return jsonify(e.message), HTTPStatus.NOT_FOUND
    except Unauthorized as e:
        return jsonify(e.message), HTTPStatus.UNAUTHORIZED
