from flask import current_app
from app.exc import InvalidKeysError, NotFoundError
from app.models import ClientModel, AddressModel
from flask_jwt_extended import (
    create_access_token,
)

class ClientServices :
    
    def check_valid_keys(data, valid_keys, key):
        
        if key not in valid_keys:
            raise InvalidKeysError(data, valid_keys)


    def get_clients():
        clients = ClientModel.query.order_by(ClientModel.name).all()

        clients = [client.serialize for client in clients]

        for client in clients:
            client["addresses"] = [address.serialize for address in client["addresses"]]
            
        return clients


    def create_client(data):
        valid_keys = ["name", "email", "password", "phone", "address"]
        for key, _ in data.items():
            ClientServices.check_valid_keys(data, valid_keys, key)
        session = current_app.db.session
        password_to_hash = data.pop("password")
        client = ClientModel(**data)
        client.password = password_to_hash
        session.add(client)
        session.commit()

        return client


    def get_token(data):
        valid_keys = ["email", "password"]

        for key, _ in data.items():
            ClientServices.check_valid_keys(data, valid_keys, key)

        user = ClientModel.query.filter_by(email=data["email"]).first()

        if not user or not user.check_password(data["password"]):
            raise NotFoundError("Bad username or password")

        return create_access_token(identity=user.id)


    def get_client_by_id(id):
        client = ClientModel.query.get(id)
        client = client.serialize
        client["addresses"] = [address.serialize for address in client["addresses"]]
        if not client:
            raise NotFoundError("Client not Found")
        return client

    def update_client(data, id):
        valid_keys = ["name", "email", "password", "phone"]
        session = current_app.db.session
        client = ClientModel.query.get(id)
        if not client:
            raise NotFoundError("Client not Found")
        for key, value in data.items():
            ClientServices.check_valid_keys(data, valid_keys, key)
            if key == "password":
                client.password = value
            else:
                setattr(client, key, value)
        session.add(client)
        session.commit()
        client = client.serialize
        client["addresses"] = [address.serialize for address in client["addresses"]]

        return client


    def delete_client(id):
        session = current_app.db.session
        client = ClientModel.query.get(id)

        session.delete(client)
        session.commit()

        return ""

    def create_address(id, data):
        session = current_app.db.session
        valid_keys = ["zip_code", "neighborhood", "street", "number", "complement", "client_id"]
        for key, _ in data.items():
            ClientServices.check_valid_keys(data, valid_keys, key)
        address = AddressModel(**data)
        session.add(address)
        session.commit()

        return address

    def get_addresses(id):
        addresses = AddressModel.query.filter_by(client_id=id).all()
        addresses = [address.serialize for address in addresses]
        return addresses

    def updade_address_by_id(data, add_id):
        session = current_app.db.session
        address = AddressModel.query.get(add_id)
        valid_keys = ["zip_code", "neighborhood", "street", "number", "complement", "client_id"]
        for key, value in data.items():
            ClientServices.check_valid_keys(data, valid_keys, key)
            setattr(address, key, value)
            session.add(address)
            session.commit()
        return address
        
    def delete_address_by_id(add_id):
        session = current_app.db.session
        address = AddressModel.query.get(add_id)
        session.delete(address)
        session.commit()
        return ""

   
    
