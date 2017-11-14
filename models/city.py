#!/usr/bin/python
""" holds class City"""
from models.base_model import BaseModel , Base
from sqlalchemy import Column, Integer, String

class City(BaseModel, Base):
    """Representation of city """
    __tablename__ = 'cities'
    state_id = Column(Integer, ForeignKey(State.id))
    name = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
