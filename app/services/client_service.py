from flask_jwt_extended import create_access_token

from app.models import ClientModel, AddressModel

from .helpers import add_commit, delete_commit, check_valid_keys, check_missed_keys

from app.exc import InvalidKeysError, NotFoundError, MissingKeysError


class ClientServices:
    @staticmethod
    def get_clients() -> list[dict]:
        clients: list[ClientModel] = ClientModel.query.order_by(ClientModel.name).all()

        clients = [client.serialize for client in clients]

        for client in clients:
            client["addresses"] = [address.serialize for address in client["addresses"]]

        return clients

    @staticmethod
    def create_client(data: dict) -> dict:
        valid_keys = ["name", "email", "password", "phone", "address"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        required_fields = ["name", "email", "password"]
        missed_fields: list[str] = check_missed_keys(data, required_fields)
        if missed_fields:
            raise MissingKeysError(required_fields, missed_fields)

        password_to_hash = data.pop("password")
        client: ClientModel = ClientModel(**data)
        client.password = password_to_hash

        add_commit(client)

        return client.serialize

    @staticmethod
    def get_token(data: dict) -> str:
        valid_keys = ["email", "password"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        required_fields = ["email", "password"]
        missed_fields: list[str] = check_missed_keys(data, required_fields)
        if missed_fields:
            raise MissingKeysError(required_fields, missed_fields)

        client: ClientModel = ClientModel.query.filter_by(email=data["email"]).first()

        if not client or not client.check_password(data["password"]):
            raise NotFoundError("Bad username or password")

        return create_access_token(identity=client.id)

    @staticmethod
    def get_client_by_id(id) -> dict:

        client: ClientModel = ClientModel.query.get(id)

        if not client:
            raise NotFoundError("Client not Found")

        client_json = client.serialize
        client_json["addresses"] = [
            address.serialize for address in client.addresses
        ]
        return client_json

    @staticmethod
    def update_client(data, id) -> dict:
        valid_keys = ["name", "email", "password", "phone"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        client: ClientModel = ClientModel.query.get(id)

        if not client:
            raise NotFoundError("Client not Found")

        for key, value in data.items():
            if key == "password":
                client.password = value
            else:
                setattr(client, key, value)

        add_commit(client)

        client_json: dict = client.serialize
        client_json["addresses"] = [
            address.serialize for address in client.addresses
        ]

        return client_json

    @staticmethod
    def delete_client(id) -> None:

        client: ClientModel = ClientModel.query.get(id)

        if not client:
            raise NotFoundError("Client not Found")

        delete_commit(client)

    @staticmethod
    def create_address(id, data):
        valid_keys = [
            "zip_code",
            "neighborhood",
            "street",
            "number",
            "complement",
            "client_id",
        ]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        address: AddressModel = AddressModel(**data)

        add_commit(address)

        return address.serialize

    @staticmethod
    def get_addresses(id):
        addresses: list[AddressModel] = AddressModel.query.filter_by(client_id=id).all()
        addresses_json: list[dict] = [address.serialize for address in addresses]

        return addresses_json

    @staticmethod
    def updade_address_by_id(data, add_id):

        valid_keys = [
            "zip_code",
            "neighborhood",
            "street",
            "number",
            "complement",
            "client_id",
        ]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        address: AddressModel = AddressModel.query.get(add_id)
        if not address:
            raise NotFoundError("Address not Found")

        for key, value in data.items():
            setattr(address, key, value)

        add_commit(address)

        return address.serialize

    @staticmethod
    def delete_address_by_id(add_id) -> None:
        address: AddressModel = AddressModel.query.get(add_id)
        if not address:
            raise NotFoundError("Address not Found")

        delete_commit(address)
