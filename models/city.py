#!/usr/bin/python
""" holds class City"""
from models.base_model import BaseModel ,Base
from sqlalchemy import Column, Integer,String
from os import getenv

class City(BaseModel, Base):
    """Representation of city """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'cities'
        state_id = Column(Integer, ForeignKey(State.id))
        name = Column(String(128), nullable=False)
        state = relationship("State", back_populates="cities")
    else:
        name = ""
        state_id = ""

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
