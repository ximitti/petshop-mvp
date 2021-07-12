from datetime import datetime
from . import db
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    date = Column(DateTime(), nullable=False, default=datetime.now())
    finished_date = Column(DateTime(), nullable=False)
    pet_delivery = Column(Boolean, nullable=False, default=False)

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "date": self.date,
            "finished_date": self.finished_date,
            "pet_delivery": self.pet_delivery,
            "pet_id": self.pet_id,
        }
