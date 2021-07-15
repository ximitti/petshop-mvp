from flask import current_app, jsonify
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.exc.status_option import InvalidKeysError
from app.models import PetshopModel
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
)