from flask_jwt_extended import create_access_token


from app.models import PetshopModel

from .helpers import add_commit, delete_commit, check_valid_keys, check_missed_keys

from app.exc import InvalidKeysError, NotFoundError, Unauthorized, MissingKeysError


class PetShopServices:
    @staticmethod
    def create_petshop(data):
        valid_keys = ["name", "email", "password", "is_admin"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        required_fields = ["name", "email", "password"]
        missed_fields: list[str] = check_missed_keys(data, required_fields)
        if missed_fields:
            raise MissingKeysError(required_fields, missed_fields)

        pet_shop: PetshopModel = PetshopModel(**data)
        add_commit(pet_shop)

        return pet_shop.serialize

    @staticmethod
    def get_petshop():

        petshops: list[PetshopModel] = PetshopModel.query.all()

        return [petshop.serialize for petshop in petshops]

    @staticmethod
    def get_petshop_by_id(id):
        pet_shop: PetshopModel = PetshopModel.query.get(id)
        if not pet_shop:
            raise NotFoundError("Petshop not found")

        return pet_shop.serialize

    @staticmethod
    def get_admin_token(data):
        valid_keys = ["email", "password"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        required_fields = ["email", "password"]
        missed_fields: list[str] = check_missed_keys(data, required_fields)
        if missed_fields:
            raise MissingKeysError(required_fields, missed_fields)

        user: PetshopModel = PetshopModel.query.filter_by(email=data["email"]).first()

        if not user or not user.check_password(data["password"]):
            raise NotFoundError("Bad username or password")

        return create_access_token(
            identity=data["email"], additional_claims={"is_admin": user.is_admin}
        )

    @staticmethod
    def update_petshop(data, email):
        valid_keys = ["name", "email", "password", "is_admin"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        pet_shop: PetshopModel = PetshopModel.query.filter_by(email=email).first()

        for key, value in data.items():

            if key == "password":
                pet_shop.password = value
            else:
                setattr(pet_shop, key, value)

        add_commit(pet_shop)

        return pet_shop.serialize

    @staticmethod
    def delete_petshop(id, email) -> None:

        petshop: PetshopModel = PetshopModel.query.filter_by(email=email).first()

        if petshop.id == id:
            raise Unauthorized("You can't delete your own user")

        petshop_to_delete: PetshopModel = PetshopModel.query.get(id)

        if not petshop_to_delete:
            raise NotFoundError("User Petshop not found")

        if petshop_to_delete.is_admin:
            raise Unauthorized("You can't delete admin users")

        delete_commit(petshop_to_delete)
