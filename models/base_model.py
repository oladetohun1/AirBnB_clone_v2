#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """
    A base class for all hbnb models

    Mapping Attributes to Table Columns
        id (sqlalchemy String): The BaseModel id.
        created_at (sqlalchemy DateTine): DateTine at creation
        updated_at (sqlalchemy DateTine): DateTine of last update
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            try:
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            except KeyError:
                self.created_at = datetime.now()

            try:
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            except KeyError:
                self.updated_at = datetime.now()

            for key, val in kwargs.items():
                if key != '__class__':
                    setattr(self, key, val)

            self.id = str(uuid.uuid4())

    def __str__(self):
        """Returns a string representation of the instance"""
        dictcopy = self.__dict__.copy()
        dictcopy.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(type(self).__name__, self.id, dictcopy)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary = (self.__dict__).copy()
        dictionary["__class__"] = str(type(self).__name__)
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
