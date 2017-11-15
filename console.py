#!/usr/bin/python3
""" console """
import models
import cmd
from copy import deepcopy
from datetime import datetime
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import re
import shlex  # for splitting the line along spaces except in double quotes

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


def is_valid_string(string):
    '''func: is fun
    '''
    # it seems that string is passed without surrounding quotes
    # non-escaped internal quotes need to be tested
    # no spaces in string
    print("+++++++++++++ TESTING VALUE STRING +++++++++++++++++")
    print("\t string = {}".format(string))
    '''
    if re.search(' ', string) is not None:
        return False

    # this doesnt test everything
    if re.search("[a-zA-Z_]+", string) is not None:
        return False
    '''
    return True


def is_valid_key(string):
    ''' func: is_valid_key
    accepts: key
    ........ not yet testing for edge cases like all underscores, other weird
    ........ stuff
    returns: boolean if string only contains alphanumberics
    ........ and underscores (no spaces)
    '''
    # if re.search('[a-zA-Z_]+', string) is None:
    # return False
    # else:
    # return True
    return True


def is_valid_integer(string):
    ''' func: is_valid_integer
    accepts: string
    returns: boolean indicating if the string represents an integer
    ........ leading or minus is allowed
    '''
    test_string = string
    if len(string) > 0 and string[0] == "-":
        test_string = string.replace('-', '', 1)
    if test_string.isdigit():
        return True
    else:
        return False


def is_valid_float(string):
    """func: is_valid_float
    accepts: string
    ........ test for int first, then for float
    Return: True is string is a simple float"""
    try:
        float(string)
        return True
    except ValueError:
        return False


def converted_string(string):
    '''func: converted_string
    accepts: value in key/value pair where type(value) == str
             leading and trailing quotes are already validated
    returns: string with leading and trailing double quotes  stripped off
    '''
    return string[1:-1]


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    prompt = '(hbnb) '

    def do_EOF(self, arg):
        """Exits console"""
        return True

    def emptyline(self):
        """ overwriting the emptyline method """
        return False

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_create(self, arg):
        """Creates a new instance of a class"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False

        if args[0] in classes:
            instance = classes[args[0]]()
        else:
            print("** class doesn't exist **")
            return False

        # here is where we handle passing params for object creation
        # we will build new list of key-value pairs where all values
        # values are validated
        arg_dict = {}
        print()
        if len(args) > 1:
            for arg in args[1:]:
                # break key/value on equal sign
                # Key must not contain an equal sign
                print("DEBUG: {}".format(str(arg)))
                key_val = arg.split('=')
                key = key_val[0]
                print("\tKEY: {}".format(key))
                val = "".join(key_val[1:])
                print("\tVALUE: {}".format(val))

                #  validate key
                if is_valid_key(key):
                    print('\tKEY_IS_ALPHA')
                else:
                    print('\tKEY__NOT__ALPHA')
                    continue

                if "id" in key:  # all id keys have strings as values
                    arg_dict[key] = val
                    continue
                if is_valid_integer(val):
                    if is_valid_float(val):
                        arg_dict[key] = float(val)  # test for leading minus
                    else:
                        arg_dict[key] = int(val)
                else:
                    if is_valid_string(val):  # not a number, valid string?
                        arg_dict[key] = val.replace('_', ' ')

        # new object has already been created, now we pass new_args into
        # do_update repeatedly to modify newly created object

        for KV in arg_dict:
            #  build arg string
            params = " ".join([args[0], instance.id, KV, str(arg_dict[KV])])
            print("---------PARAMS------------")
            print(params)
            print("---------------------------")
            self.do_update(params)

        print(instance.id)
        instance.save()

    def do_show(self, arg):
        """Prints an instance as a string based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    print(models.storage.all()[key])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """Deletes an instance based on the class and id"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                key = args[0] + "." + args[1]
                if key in models.storage.all():
                    models.storage.all().pop(key)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """Prints string representations of instances"""
        args = shlex.split(arg)
        obj_list = []
        if len(args) == 0:
            for value in models.storage.all().values():
                obj_list.append(str(value))
            print("[", end="")
            print(", ".join(obj_list), end="")
            print("]")
        elif args[0] in classes:
            for key in models.storage.all():
                if args[0] in key:
                    obj_list.append(str(models.storage.all()[key]))
            print("[", end="")
            print(", ".join(obj_list), end="")
            print("]")
        else:
            print("** class doesn't exist **")

    def do_update(self, arg):
        """Update an instance based on the class name, id, attribute & value"""
        args = shlex.split(arg)
        integers = ["number_rooms", "number_bathrooms", "max_guest",
                    "price_by_night"]
        floats = ["latitude", "longitude"]
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] in classes:
            if len(args) > 1:
                k = args[0] + "." + args[1]
                if k in models.storage.all():
                    if len(args) > 2:
                        if len(args) > 3:
                            if args[0] == "Place":
                                if args[2] in integers:
                                    try:
                                        args[3] = int(args[3])
                                    except:
                                        args[3] = 0
                                elif args[2] in floats:
                                    try:
                                        args[3] = float(args[3])
                                    except:
                                        args[3] = 0.0
                            setattr(models.storage.all()[k], args[2], args[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
