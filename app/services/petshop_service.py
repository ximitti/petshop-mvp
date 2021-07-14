from flask import current_app
from http import HTTPStatus

from app.models import PetshopModel


def create_petshop(data):
    session = current_app.db.session

    pet_shop = PetshopModel(**data)

    session.add(pet_shop)
    session.commit()

    return pet_shop.serialize, HTTPStatus.CREATED
