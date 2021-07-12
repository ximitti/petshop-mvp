from . import db
from sqlalchemy import Column, String, Integer, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref


class AddressModel(db.Model):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)

    zip_code = Column(String(10), nullable=False, unique=True)
    neighborhood = Column(String(150), nullable=False)
    street = Column(String(150), nullable=False)
    number = Column(String(5), nullable=False)
    complement = Column(String(150))
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "zip_code": self.zip_code,
            "neighborhood": self.neighborhood,
            "street": self.street,
            "number": self.number,
            "complement": self.complement,
            "client_id": self.client_id,
        }
