#!/usr/bin/python3
""" Console Module """
import cmd
import json
import sys
from models.base_model import BaseModel, Base
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) '  # if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, args):
        """ Create an object of any class"""

        totargs = args.split()
        params = {}
        classname = totargs[0]

        if not args:
            print("** class name missing **")
            return
        elif classname not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        for eachparam in totargs[1:]:
            if ("=" not in eachparam):
                continue

            key, value = eachparam.split("=", 1)

            if value.startswith('"') & value.endswith('"'):
                value = value.strip('"').replace("_", " ")
                value = value.replace('\\"', '"')
            else:
                try:
                    value = float(value)
                except ValueError:
                    try:
                        value = int(value)
                    except ValueError:
                        continue
            params[key] = value

        try:
            obj = eval(classname)(**params)
            storage.new(obj)
            storage.save()
            print(obj.id)
        except TypeError:
            return

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.split(" ")

        # guard against trailing args

        if len(new) < 1:
            print("** class name missing **")
            return
        c_name = new[0]
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if len(new) < 2:
            print("** instance id missing **")
            return

        c_id = new[1]
        c_name = new[0]
        key = c_name + "." + c_id
        c_name = eval(c_name)
        try:
            print(storage.all(c_name)[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.split(" ")
        c_name = new[0]
        c_id = new[1]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del (storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        new = args.split(" ")
        c_name = new[0]
        if c_name:
            if c_name not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            c_name = eval(c_name)
            o = storage.all(c_name)
            print([str(str(o[k])) for k in o])
        else:
            o = storage.all()
            print([str(str(o[k])) for k in o])

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        arg = args.split(" ")
        count = 0
        for objs in storage.all().values():
            if arg[0] == objs.__class__.__name__:
                count += 1
        print(count)

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """

        # isolate cls from id/args, ex: (<cls>, delim, <id/args>)
        args = args.split(" ")
        if args[0]:
            c_name = args[0]
        else:  # class name not present
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return
        # isolate id from args
        if len(args) < 2:  # id not present
            print("** instance id missing **")
            return

        c_id = args[1]
        key = c_name + "." + c_id
        if key not in storage.all():
            print("** no instance found **")
            return

        new_dict = storage.all()[key]
        if len(args) < 3:
            print("** attribute name missing **")
            return

        att_name = args[2]
        if len(args) < 4:
            print("*** value missing **")
            return
        att_val = args[3]

        # validate attribute
        if att_name in HBNBCommand.types:
            try:
                att_val = HBNBCommand.types[att_name](att_val)
            except ValueError:
                print("** invalid value for attribute {} **".format(att_name))
                return

        # Update dictionary with namr, value
        setattr(new_dict, att_name, att_val)
        new_dict.save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
