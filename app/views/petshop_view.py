from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from http import HTTPStatus

from sqlalchemy.exc import IntegrityError
from app.exc import Unauthorized, InvalidKeysError, NotFoundError, MissingKeysError

from app.services import PetShopServices
from app.services.helpers import is_admin


bp = Blueprint("bp_petshop", __name__, url_prefix="/api")


@bp.get("/petshop")
@jwt_required()
def get() -> tuple:
    try:
        is_admin(get_jwt())
        pet_shops: list[dict] = PetShopServices.get_petshop()

        return (
            jsonify(data=pet_shops),
            HTTPStatus.OK,
        )
    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )


@bp.post("/petshop/register")
def register() -> tuple:
    try:
        pet_shop: dict = PetShopServices.create_petshop(request.get_json())

        return (
            jsonify(data=pet_shop),
            HTTPStatus.CREATED,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except IntegrityError as _:
        return (
            jsonify(error="Petshop already exists"),
            HTTPStatus.BAD_REQUEST,
        )

    except MissingKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )


@bp.post("/petshop/login")
def login() -> tuple:
    try:
        access_token: str = PetShopServices.get_admin_token(request.get_json())

        return (
            jsonify(data={"access_token": access_token}),
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

    except MissingKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )


@bp.get("/petshop/<int:petshop_id>")
@jwt_required()
def get_by_id(petshop_id: int) -> tuple:
    try:
        is_admin(get_jwt())
        pet_shop: dict = PetShopServices.get_petshop_by_id(petshop_id)

        return (
            jsonify(data=pet_shop),
            HTTPStatus.OK,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )


@bp.patch("/petshop")
@jwt_required()
def patch() -> tuple:
    try:
        is_admin(get_jwt())
        data = request.get_json()
        email = get_jwt_identity()
        pet_shop: dict = PetShopServices.update_petshop(data, email)

        return (
            jsonify(data=pet_shop),
            HTTPStatus.OK,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )

    except InvalidKeysError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )

    except IntegrityError as _:
        return (
            jsonify(error="Petshop already exists"),
            HTTPStatus.BAD_REQUEST,
        )


@bp.delete("/petshop/<int:petshop_id>")
@jwt_required()
def delete(petshop_id: int) -> tuple:
    try:
        is_admin(get_jwt())
        email: str = get_jwt_identity()

        PetShopServices.delete_petshop(petshop_id, email)

        return (
            "",
            HTTPStatus.NO_CONTENT,
        )

    except Unauthorized as e:
        return (
            jsonify(e.message),
            HTTPStatus.UNAUTHORIZED,
        )

    except NotFoundError as e:
        return (
            jsonify(e.message),
            HTTPStatus.BAD_REQUEST,
        )
