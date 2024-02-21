#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

from models.base_model import Base
import os

HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
HBNB_ENV = os.getenv('HBNB_ENV')


class DBStorage:
    """This class manages storage of hbnb models in JSON format"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the db engine
        """
        self.__engine = create_engine(
            f"mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@"
            f"{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}",
            pool_pre_ping=True)

        if HBNB_ENV == 'test':
            Base.meta.drop_all(self.__engine)

        self.reload()

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage

        Keyword Arguments:
            cls -- If specified, one type of class has to be
                returned (default: {None})

        Returns:
            List of objects.
        """
        all_objects = {}

        if cls is not None:
            if self.__session is not None:
                instances = self.__session.query(cls).all()
                for instance in instances:
                    all_objects.update({instance.to_dict()['__class__']
                                        + '.' + instance.id: instance})

        else:

            all_cls = [User, Place, State, City, Amenity, Review]

            for _cls in all_cls:
                if self.__session is not None:
                    instances = self.__session.query(_cls).all()
                    for instance in instances:
                        all_objects.update({instance.to_dict()['__class__']
                                            + '.' + instance.id: instance})

        return all_objects

    def new(self, obj):
        """Adds new object to the session"""
        if self.__session is not None:
            self.__session.add(obj)

    def save(self):
        """Dump the session to the db"""
        if self.__session is not None:
            self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the session if it's inside.

        Keyword Arguments:
            obj -- Object to be deleted. (default: {None})
        """
        if obj is not None:
            if self.__session is not None:
                self.__session.query(obj).delete()

    def reload(self):
        """creates a new session"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)()
