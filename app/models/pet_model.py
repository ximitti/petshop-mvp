from . import db
from sqlalchemy import Column, String, Integer, Text, ForeignKey


class PetModel(db.Model):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True)

    name = Column(String(50), nullable=False)
    species = Column(String(50), nullable=False)
    size = Column(String(50), nullable=False)
    allergy = Column(String(50), nullable=False)
    breed = Column(String(50))
    fur = Column(String(50))
    photo_url = Column(Text())

    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "allergy": self.allergy,
            "breed": self.breed,
            "fur": self.fur,
            "photo_url": self.photo_url,
            "client_id": self.client_id,
        }
