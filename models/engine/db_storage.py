#!/usr/bin/python3
"""MYSQL Storage"""
from models.base_model import Base, BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship
from os import getenv


class DBStorage:
    """
    Represents a new engine/storage MYSQL
    Attributes:
        __engine: Set to None
        __session: Set to None
    Instance Methods:
        __init__(self) - Initialize class
        all(self, cls=None) - Query db for all objects related to the cls
        new(self, obj) - Add obj to current db session (seld.__session)
        save(self) - Commit changes pf current db session (self.__session)
        delete(self, obj=None) - Delete from current db session obj if != None
        reload(self) - Create all tables of db
                     - Create current db session (self.__session) from
                     (self.__engine)
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize instance"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

        if (getenv("HBNB_ENV") == "test"):
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Queries the database session for all objects related to cls"""
        if (cls is None):
            objs = self.__session.query(User).all()
            objs.extend(self.__session.query(State).all())
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(Amenity).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())

        else:
            objs = self.__session.query(cls).all()

        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all charges of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj"""
        if (obj is not None):
            self.__session.delete(obj)

    def reload(self):
        """Create all tables from database, create current database session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Method on private session attribute"""
        self.__session.remove()
