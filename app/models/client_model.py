from sqlalchemy.sql.expression import delete
from . import db
from sqlalchemy import Column, String, Integer
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship, backref


class ClientModel(db.Model):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)

    email = Column(String(150), nullable=False, unique=True)
    name = Column(String(150), nullable=False)
    password_hash = Column(String(150), nullable=False)
    phone = Column(String(16))

    addresses = relationship(
        "AddressModel", backref=backref("client", uselist=False)
    )

    @property
    def password(self):
        raise ArithmeticError("Password is not acessible")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "email": self.email,
            "name": self.name,
            "phone": self.phone,
            "addresses": self.addresses,
        }
