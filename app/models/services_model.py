from . import db
from sqlalchemy import Column, String, Integer, Text, Float


class ServicesModel(db.Model):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)
    description = Column(Text(), nullable=False)
    price = Column(Float(), nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
        }
