from app.models.services_model import ServicesModel
from app.exc.status_not_found import NotFoundError
from app.exc.status_option import InvalidKeysError
from http import HTTPStatus
from flask import current_app
from flask_jwt_extended import (
    get_jwt_identity,
)

def check_valid_keys(data, valid_keys, key):
    if key not in valid_keys:
        raise InvalidKeysError(data, valid_keys)

def get_services():
    services: ServicesModel =  ServicesModel.query.all()
    return services

def create_service(data):
    valid_keys = ["name", "description", "price"]
    for key, _ in data.items():
        check_valid_keys(data, valid_keys, key)

    session = current_app.db.session
    service: ServicesModel = ServicesModel(**data)
    session.add(service)
    session.commit()
    return service

def get_service_by_id(service_id: int):
    current_service_id = get_jwt_identity()
    if current_service_id == id:
        service: ServicesModel = ServicesModel.query.get(service_id)
        if not service:
             raise NotFoundError("Service not found")
        return service
    return HTTPStatus.UNAUTHORIZED

def update_service(data, service_id: int):
    current_service_id = get_jwt_identity()
    if current_service_id == id:
        service = get_service_by_id(service_id)
        session = current_app.db.session
        valid_keys = ["name", "description", "price"]
        for key, value in data.items():
            check_valid_keys(data, valid_keys, key)

            setattr(service, key, value)

        session.add(service)
        session.commit()

        if not service:
             raise NotFoundError("Service not found")
        return service
    return HTTPStatus.UNAUTHORIZED

def delete_service(service_id: int):
    session = current_app.db.session
    service = ServicesModel.query.get(service_id)    
    if not service:
            raise NotFoundError("Service not found")

    service: ServicesModel = ServicesModel.query.get(service_id)
    
    session.delete(service)
    session.commit()

    return ""

