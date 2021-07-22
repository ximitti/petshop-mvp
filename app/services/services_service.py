from app.models.services_model import ServicesModel

from app.exc import NotFoundError, InvalidKeysError, MissingKeysError

from .helpers import add_commit, delete_commit, check_valid_keys, check_missed_keys


class ServiceServices:
    @staticmethod
    def get_services() -> list[dict]:
        services: ServicesModel = ServicesModel.query.all()

        return [service.serialize for service in services]

    @staticmethod
    def create_service(data) -> dict:
        valid_keys = ["name", "description", "price"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        required_fields = ["name", "description", "price"]
        missed_fields: list[str] = check_missed_keys(data, required_fields)
        if missed_fields:
            raise MissingKeysError(required_fields, missed_fields)

        service: ServicesModel = ServicesModel(**data)
        add_commit(service)

        return service.serialize

    @staticmethod
    def get_service_by_id(service_id: int) -> dict:
        service: ServicesModel = ServicesModel.query.get(service_id)

        if not service:
            raise NotFoundError("Service not found")

        return service.serialize

    @staticmethod
    def update_service(data, service_id: int) -> dict:
        valid_keys = ["name", "description", "price"]

        if check_valid_keys(data, valid_keys):
            raise InvalidKeysError(data, valid_keys)

        service: ServicesModel = ServicesModel.query.get(service_id)

        if not service:
            raise NotFoundError("Service not found")

        for key, value in data.items():
            setattr(service, key, value)

        add_commit(service)

        return service.serialize

    @staticmethod
    def delete_service(service_id: int) -> None:
        service: ServicesModel = ServicesModel.query.get(service_id)

        if not service:
            raise NotFoundError("Service not found")

        delete_commit(service)
