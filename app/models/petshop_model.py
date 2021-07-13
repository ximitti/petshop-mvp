from . import db
from sqlalchemy import Column, String, Integer, Boolean


class PetshopModel(db.Model):
    __tablename__ = "petshops"

    id = Column(Integer, primary_key=True)

    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    id_admin = Column(Boolean(), default=True)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "id_admin": self.id_admin,
        }
