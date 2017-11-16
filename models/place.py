#!/usr/bin/python
""" holds class Place"""
from models.base_model import BaseModel, Base
import  models
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

class Place(BaseModel):
    """Representation of Place """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=False)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        reviews =  relationship("Review", cascade="all,delete", backref="user")
    else:
        amenity_ids = []

        @property
        def reviews(self):
            """returns Cities instances of current state_id"""
            reviews = []
            objs = models.storage.all(models.review.Review)
            for key in objs:
                if objs[key].place_id == self.id:
                    cities.append(objs[key])
            return reviews

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        self.city_id = kwargs.pop('city_id', "")
        self.user_id = kwargs.pop('user_id', "")
        self.name = kwargs.pop('name', "")
        self.description = kwargs.pop('description', "")
        self.number_rooms = int(kwargs.pop('number_rooms', 0))
        self.number_bathrooms = int(kwargs.pop('number_bathrooms', 0))
        self.max_guest = int(kwargs.pop('max_guest', 0))
        self.price_by_night = int(kwargs.pop('price_by_night', 0))
        self.latitude = float(kwargs.pop('latitude', 0.0))
        self.longitude = float(kwargs.pop('longitude', 0.0))
        super().__init__(*args, **kwargs)
