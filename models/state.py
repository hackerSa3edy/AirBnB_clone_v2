#!/usr/bin/python3
"""
This module defines the State class for the HBNB project.

Imports:
    BaseModel: Base class for all HBNB models.
    Base: Base class for SQLAlchemy models.
    Column, String: SQLAlchemy classes and functions to manage table columns.
    relationship: SQLAlchemy function to create relationships between tables.
    models: Module that contains the application models.
    os: Module that provides a way of using operating system dependent
    functionality.

Classes:
    State: This class represents a State in the HBNB project.
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
import os


class State(BaseModel, Base):
    """
    This class represents a State in the HBNB project.

    Inherits from:
        BaseModel: Base class for all HBNB models.
        Base: Base class for SQLAlchemy models.

    Attributes:
        __tablename__ (str): The name of the table to use for this class.
        name (Column): The name of the state. It is a SQLAlchemy Column of
        type String with a maximum length of 128 characters, and it cannot
        be null.
        cities (relationship): A SQLAlchemy relationship that represents all
        City instances associated with this State instance. When a State
        instance is deleted, all of its associated City instances are also
        deleted.
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship(
        'City',
        cascade='all, delete',
        backref='state'
        )

    if os.getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def cities(self):
            """
            Returns a list of City instances with the same state_id as the
            current State instance.

            This method is part of the State class that represents a state in
            the hbnb clone.

            Parameters: None

            Returns:
                list: A list of City instances with the same state_id as the
                current State instance.
            """
            cities_to_curr_state = models.storage.all(models.City).values()
            cities_to_curr_state = [
                city for city in list(cities_to_curr_state)
                if city.state_id == self.id
            ]
            return cities_to_curr_state
