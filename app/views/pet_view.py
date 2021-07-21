from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from http import HTTPStatus

from app.exc import Unauthorized, InvalidKeysError, NotFoundError, MissingKeysError

from app.services import PetServices
from app.services.helpers import is_admin, check_authorization


bp = Blueprint("bp_pet", __name__, url_prefix="/api")


@bp.post("/pets/")
@jwt_required()
def create() -> tuple:
    try:

        data = request.get_json()
        check_authorization(data.get("client_id"), get_jwt_identity())

        pet: dict = PetServices.create_pet(data)

        return (
            jsonify(data=pet),
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


@bp.get("/pets/")
@jwt_required()
def retrieve_all() -> tuple:
    client_id = request.args.get("client_id")
    pets: list[dict] = PetServices.get_pets(client_id)

    return (
        jsonify(data=pets),
        HTTPStatus.OK,
    )


@bp.get("/pets/<int:pet_id>")
@jwt_required()
def retrieve_by_id(pet_id: int) -> tuple:
    try:
        pet: dict = PetServices.get_pet_by_id(pet_id)

        return (
            jsonify(data=pet),
            HTTPStatus.OK,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
        )


@bp.patch("/pets/<int:pet_id>")
@jwt_required()
def update(pet_id: int) -> tuple:
    try:
        is_admin(get_jwt())

        pet_to_get_owner: dict = PetServices.get_pet_by_id(pet_id)
        check_authorization(pet_to_get_owner.get("client_id"), get_jwt_identity())

        pet: dict = PetServices.update_pet(request.get_json(), pet_id)

        return (
            jsonify(data=pet),
            HTTPStatus.OK,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.NOT_FOUND,
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


@bp.delete("/pets/<int:pet_id>")
@jwt_required()
def delete(pet_id: int) -> tuple:
    try:
        is_admin(get_jwt())

        pet_to_get_owner: dict = PetServices.get_pet_by_id(pet_id)
        check_authorization(pet_to_get_owner.get("client_id"), get_jwt_identity())

        PetServices.delete_pet(pet_id)
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


@bp.get("/pets/<int:pet_id>/orders")
@jwt_required()
def get_orders_by_pet(pet_id: int) -> tuple:
    try:

        pet: dict = PetServices.get_pet_by_id(pet_id)

        check_authorization(pet.get("client_id"), get_jwt_identity())

        orders: list[dict] = PetServices.get_pet_orders(pet_id)

        return (
            jsonify(data=orders),
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
