#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv


if (getenv("HBNB_TYPE_STORAGE") == "db"):
    from .engine.db_storage import DBStorage
    storage = DBStorage()
elif (getenv("HBNB_TYPE_STORAGE") == "FileStorage"):
    from .engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
