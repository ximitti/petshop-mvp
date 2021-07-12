from . import db
from sqlalchemy import Column, String, Integer, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref


class ClientModel(db.Model):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)

    email = Column(String(150), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    password = Column(String(150), nullable=False)
    phone = Column(String(16))
    address_id = Column(Integer, ForeignKey("address.id"), nullable=False)

    addresses = relationship(
        "AddressModel", backref=backref("client", uselist=False)
    )

    @property
    def password(self):
        raise ArithmeticError("Password is not acessible")

    @password.setter
    def password(self, password_to_hash):
        self.password = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password, password_to_compare)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "phone": self.phone,
            "address_id": self.address_id,
            "addresses": self.addresses,
        }
