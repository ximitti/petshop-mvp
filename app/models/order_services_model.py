from . import db
from sqlalchemy import Column, Integer, ForeignKey


class OrderServicesModel(db.Model):
    __tablename__ = "order_services"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    services_id = Column(Integer, ForeignKey("services.id"))
