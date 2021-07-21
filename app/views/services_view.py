from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt
from http import HTTPStatus

from app.services.helpers import is_admin
from app.services import ServiceServices

from app.exc import InvalidKeysError, NotFoundError, Unauthorized, MissingKeysError


bp = Blueprint("bp", __name__, url_prefix="/api")


@bp.get("/services/")
def get() -> tuple:
    services: list[dict] = ServiceServices.get_services()

    return (
        jsonify(data=services),
        HTTPStatus.OK,
    )


@bp.post("/services/")
@jwt_required()
def create() -> tuple:
    try:
        is_admin(get_jwt())

        service: dict = ServiceServices.create_service(request.get_json())

        return (
            jsonify(data=service),
            HTTPStatus.CREATED,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )

    except MissingKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )


@bp.get("/services/<int:service_id>")
@jwt_required()
def retrieve_by_id(service_id: int) -> tuple:
    try:
        is_admin(get_jwt())

        service: dict = ServiceServices.get_service_by_id(service_id)

        return (
            jsonify(data=service),
            HTTPStatus.OK,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )


@bp.patch("/services/<int:service_id>")
@jwt_required()
def update_service_by_id(service_id: int) -> tuple:
    try:
        is_admin(get_jwt())

        service: dict = ServiceServices.update_service(request.get_json(), service_id)

        return (
            jsonify(data=service),
            HTTPStatus.OK,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
        )


@bp.delete("/services/<int:service_id>")
@jwt_required()
def delete_service_by_id(service_id: int) -> tuple:
    try:
        is_admin(get_jwt())

        ServiceServices.delete_service(service_id),

        return (
            "",
            HTTPStatus.NO_CONTENT,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )
