#!/usr/bin/python3
"""DBStorage mode"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User
from models.review import Review
from models.base_model import Base


class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None
    types = [User, State, City, Amenity, Place, Review]

    def __init__(self):
        """Initialize method"""
        self.__engine = create_engine('mysql://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'), 
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'), 
                                              getenv('HBNB_MYSQL_DB')))
        if getenv('HBNB_MYSQL_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query all objs"""
        dict = {}
        if cls is None:
            for type in types:
                for obj in self.__session.query(type).all():
                    key = "{}.{}".format(type.__class__, obj.id)
                    dict[key] = obj
        else:
            for obj in self.__session.query(cls):
                key = "{}.{}".format(cls.__class__, obj.id)
                dict[key] = obj
        return dict

    def new(self, obj):
        """adds an object"""
        self.__session.add(obj)

    def save(self):
        """commits changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes obj"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all table in database and session"""
        Base.metadata.create_all(self.__engine)
        self.__Session = sessionmaker(bind=self.__engine, 
                                      expire_on_commit=False)
        self.__session = scoped_session(self.__Session)
