#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy.orm import relationship
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table


association_table = Table("place_amenity", Base.metadata,
                          Column("place_id",
                                 String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place",
                           cascade="all, delete")
    amenities = relationship("Amenity",
                             secondary="association_table",
                             viewonly=False,
                             overlaps="place_amenities")
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """FileStorage getter attribute"""
            revlist = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    revlist.append(review)
            return revlist

        @property
        def amenities(self):
            """
            Returns a list of Amenity instances based on attribute amenity_ids
            """
            amelist = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id == self.amenity_ids:
                    amelist.append(amenity)
            return amelist

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
