#!/usr/bin/python3
""" Defines the HBNB console."""
from io import StringIO
from unittest.mock import patch
from os import remove
import unittest
import os
import console
import tests


from console import HBNBCommand
from models import storage
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


classes = ["BaseModel", "User", "State"]


class TestConsole(unittest.TestCase):
    """Unittest to test console"""

    def setUp(self):
        """Set up method"""
        try:
            remove("file.json")
        except FileNotFoundError:
            pass

    def test_docstring_in_console(self):
        """Test documentation"""
        self.assertIsNotNone(console.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.do_count.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_quit(self):
        """Test do_quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            self.assertEqual('', f.getvalue())

    def test_create(self):
        """Test do_create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create ")
            self.assertEqual("** class name missing **\n", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create addwdq")
            self.assertEqual("** class does not exist **\n", f.getvalue())

        for i in classes:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd("create " + i)
                id = f.getvalue()
                curdict = storage.all()
                self.assertTrue((i + "." + id[:-1]) in curdict.keys())

    def test_show(self):
        """Test do_show command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())


if __name__ == '__main__':
    unittest.main()
