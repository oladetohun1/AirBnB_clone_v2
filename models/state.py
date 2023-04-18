#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
import models
from models.city import City
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    """if (getenv("HBNB_TYPE_STORAGE") == "FileStorage"):"""
    @property
    def cities(self):
        """Get a list of all cities related to State object"""
        cities_list = []
        for city in list(models.storage.all(City).values()):
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list
