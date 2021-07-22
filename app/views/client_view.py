from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from http import HTTPStatus

from app.services import ClientServices
from app.services.helpers import is_admin, check_authorization

from app.exc import InvalidKeysError, Unauthorized, NotFoundError, MissingKeysError
from sqlalchemy.exc import IntegrityError


bp = Blueprint("bp_client", __name__, url_prefix="/api")


@bp.get("/clients")
@jwt_required()
def get_clients() -> tuple:
    try:
        is_admin(get_jwt())
        clients: list[dict] = ClientServices.get_clients()

        return (
            jsonify(data=clients),
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


@bp.post("/clients/register")
def create_client() -> tuple:
    try:
        client: dict = ClientServices.create_client(request.get_json())

        return (
            jsonify(data=client),
            HTTPStatus.CREATED,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except MissingKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )


@bp.post("/clients/login")
def login() -> tuple:
    try:
        token: str = ClientServices.get_token(request.get_json())

        return (
            jsonify(data={"access_token": token}),
            HTTPStatus.OK,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except MissingKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
        )


@bp.get("/clients/<int:client_id>")
@jwt_required()
def get_client_by_id(client_id: int) -> tuple:
    try:
        if not check_authorization(client_id, get_jwt_identity()):
            is_admin(get_jwt())

        client: dict = ClientServices.get_client_by_id(client_id)

        return (
            jsonify(data=client),
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


@bp.patch("/clients/<int:client_id>")
@jwt_required()
def update_client_by_id(client_id: int) -> tuple:
    try:
        if not check_authorization(client_id, get_jwt_identity()):
            is_admin(get_jwt())

        client: dict = ClientServices.update_client(request.get_json(), client_id)

        return jsonify(data=client)

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
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


@bp.delete("/clients/<int:client_id>")
@jwt_required()
def delete_client_by_id(client_id: int) -> tuple:
    try:
        if not check_authorization(client_id, get_jwt_identity()):

            is_admin(get_jwt())

        ClientServices.delete_client(client_id)

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


@bp.post("/clients/<int:client_id>/address")
@jwt_required()
def create_address(client_id: int) -> tuple:
    try:
        check_authorization(client_id, get_jwt_identity())

        data = request.get_json()
        data["client_id"] = client_id

        address: dict = ClientServices.create_address(client_id, data)

        return (
            jsonify(data=address),
            HTTPStatus.CREATED,
        )

    except IntegrityError as _:
        return (
            jsonify(error="already exists"),
            HTTPStatus.NOT_ACCEPTABLE,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )


@bp.get("/clients/<int:client_id>/address")
@jwt_required()
def get_address(client_id: int) -> tuple:
    try:
        check_authorization(client_id, get_jwt_identity())

        addresses: list[dict] = ClientServices.get_addresses(client_id)

        return (
            jsonify(data=addresses),
            HTTPStatus.OK,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )


@bp.patch("/clients/<int:client_id>/address/<int:add_id>")
@jwt_required()
def update_address(client_id: int, add_id: int) -> tuple:
    try:
        check_authorization(client_id, get_jwt_identity())

        data = request.get_json()

        address: dict = ClientServices.updade_address_by_id(data, add_id)

        return (
            jsonify(data=address),
            HTTPStatus.OK,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
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


@bp.delete("/clients/<int:client_id>/address/<int:add_id>")
@jwt_required()
def delete_edit_address(client_id: int, add_id: int) -> tuple:
    try:
        check_authorization(client_id, get_jwt_identity())

        ClientServices.delete_address_by_id(add_id)

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
