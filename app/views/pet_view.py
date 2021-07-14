from app.models.pet_model import PetModel
from flask import Blueprint, jsonify, current_app

bp = Blueprint("bp_pet", __name__, url_prefix="/pets")

