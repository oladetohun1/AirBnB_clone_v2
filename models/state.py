#!/usr/bin/python3
""" State Module for HBNB project """
import os
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)

    cities = relationship("City", backref="state",
                          cascade="all, delete")

    if (os.getenv("HBNB_TYPE_STORAGE") != "db"):
        @property
        def cities(self):
            """City list"""
            from models import storage
            return [city for city in storage.all('City').values()
                    if city.state_id == self.id]
