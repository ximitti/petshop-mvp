from . import db
from sqlalchemy import Column, String, Integer, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass


@dataclass
class PetshopModel(db.Model):
    id: int
    name: str
    email: str
    is_admin: bool

    __tablename__ = "petshops"

    id = Column(Integer, primary_key=True)

    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(150), nullable=False)
    is_admin = Column(Boolean(), default=True)

    @property
    def password(self):
        raise AttributeError("Password is not acessible")

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_admin": self.is_admin,
        }
