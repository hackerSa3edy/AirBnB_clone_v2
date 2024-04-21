#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
import os


class State(BaseModel, Base):
    """ State class """
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
