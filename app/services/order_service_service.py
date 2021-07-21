from app.models import OrderServicesModel

from .helpers import add_commit


class OrderServiceServices:
    @staticmethod
    def create_order_service(order_id: int, service_id: int) -> None:

        order_service: OrderServicesModel = OrderServicesModel(
            order_id=order_id, services_id=service_id
        )

        add_commit(order_service)
