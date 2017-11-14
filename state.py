 #!/usr/bin/python
""" holds class State"""
from models.base_model import BaseModel, Base
from models.engine.file_storage import FileStorage
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from os import getenv

class State(BaseModel, Base):
    """Representation of state """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", back_populates="state")
    else:
        name = ""
        
    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)

    @property
    def cities(self):
        """returns Cities instances of current state_id"""
        cities = []
        objs = FileStorage.all()
        for key in objs:
            if "City" in key and objs[key].state_id == self.id:
                cities.append(objs[key])
        return cities
