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

#    def preloop(self):
#        """Prints if isatty is false"""
#        if not sys.__stdin__.isatty():
#            print('(hbnb)')
#
#    def precmd(self, line):
#        """Reformat command line for advanced command syntax.
#
#        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
#        (Brackets denote optional fields in usage example.)
#        """
#        _cmd = _cls = _id = _args = ''  # initialize line elements
#
#        # scan for general formating - i.e '.', '(', ')'
#        if not ('.' in line and '(' in line and ')' in line):
#            return line
#
#        try:  # parse line left to right
#            pline = line[:]  # parsed line
#
#            # isolate <class name>
#            _cls = pline[:pline.find('.')]
#
#            # isolate and validate <command>
#            _cmd = pline[pline.find('.') + 1:pline.find('(')]
#            if _cmd not in HBNBCommand.dot_cmds:
#                raise Exception
#
#            # if parantheses contain arguments, parse them
#            pline = pline[pline.find('(') + 1:pline.find(')')]
#            if pline:
#                # partition args: (<id>, [<delim>], [<*args>])
#                pline = pline.partition(', ')  # pline convert to tuple
#
#                # isolate _id, stripping quotes
#                _id = pline[0].replace('\"', '')
#                # possible bug here:
#                # empty quotes register as empty _id when replaced
#
#                # if arguments exist beyond _id
#                pline = pline[2].strip()  # pline is now str
#                if pline:
#                    # check for *args or **kwargs
#                    if pline[0] == '{' and pline[-1] == '}'\
#                            and type(eval(pline)) is dict:
#                        _args = pline
#                    else:
#                        _args = pline.replace(',', '')
#                        # _args = _args.replace('\"', '')
#            line = ' '.join([_cmd, _cls, _id, _args])
#
#        except Exception:
#            pass
#        finally:
#            return line
#
#    def postcmd(self, stop, line):
#        """Prints if isatty is false"""
#        if not sys.__stdin__.isatty():
#            print('(hbnb) ', end='')
#        return stop
#
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
            print([str(o[k]) for k in o])
        else:
            o = storage.all()
            print([str(o[k]) for k in o])

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
