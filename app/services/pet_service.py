from app.exc import InvalidKeysError, NotFoundError, MissingKeysError, PetExistsError

from app.models import OrderModel, PetModel

from .helpers import (
    add_commit,
    delete_commit,
    check_valid_keys,
    check_missed_keys,
)


class PetServices:
    @staticmethod
    def create_pet(data) -> dict:
        valid_keys = [
            "name",
            "species",
            "size",
            "allergy",
            "breed",
            "fur",
            "photo_url",
            "client_id",
        ]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        required_fields = [
            "name",
            "species",
            "size",
            "allergy",
            "client_id",
        ]
        missed_fields: list[str] = check_missed_keys(data, required_fields)
        if missed_fields:
            raise MissingKeysError(required_fields, missed_fields)

        pets: list[PetModel] = PetModel.query.filter_by(
            client_id=data.get("client_id")
        ).all()

        for pet in pets:
            if pet.name == data.get("name"):
                raise PetExistsError("Pet already exists")

        pet: PetModel = PetModel(**data)

        add_commit(pet)

        return pet.serialize

    @staticmethod
    def get_pets(client_id: int) -> list:

        if client_id:
            pets: list[PetModel] = PetModel.query.filter_by(client_id=client_id).all()
        else:
            pets: list[PetModel] = PetModel.query.all()

        pets: list[dict] = [pet.serialize for pet in pets]

        return pets

    @staticmethod
    def get_pet_by_id(pet_id: int) -> dict:
        pet: PetModel = PetModel.query.get(pet_id)

        if not pet:
            raise NotFoundError("Pet not found")

        return pet.serialize

    @staticmethod
    def get_pet_orders(pet_id: int):
        orders: OrderModel = OrderModel.query.filter_by(pet_id=pet_id).all()
        orders: list[dict] = [order.serialize for order in orders]

        return orders

    @staticmethod
    def update_pet(data: dict, pet_id: int):
        valid_keys = [
            "name",
            "species",
            "size",
            "allergy",
            "breed",
            "fur",
            "photo_url",
            "client_id",
        ]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        pet: PetModel = PetModel.query.get(pet_id)
        if not pet:
            raise NotFoundError("Pet not found")

        for key, value in data.items():
            setattr(pet, key, value)

        add_commit(pet)

        return pet.serialize

    @staticmethod
    def delete_pet(pet_id: int) -> None:
        pet: PetModel = PetModel.query.get(pet_id)

        if not pet:
            raise NotFoundError("Pet not found")

        delete_commit(pet)
