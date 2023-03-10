#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
A command line interpreter for the AirBnB objects.
Type help to get all commands
"""

import cmd
from models import storage
from exports import valid_classes, BaseModel
from ast import literal_eval


class HBNBCommand(cmd.Cmd):
    """A representation of the command line interpreter
    Attributes:
    - prompt: A string to print as prompt
    """

    prompt = "(hbnb) "

    def preloop(self):
        """Set interpreter-wide attributes"""
        self.available = {"BaseModel": BaseModel}
        self.valid_commands = {
            "all": self.do_all,
            "count": self._count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
        }

    def emptyline(self):
        """Does nothing when the user enters an empty line"""
        return

    def do_EOF(self, line):
        """Exits the interpreter"""
        print()  # arfs6: printing new line character
        return self.close()

    def do_quit(self, line):
        """quit: Exits the interpreter"""
        return self.close()

    def close(self):
        """Does clean up tasks an exits the interpreter"""
        return True

    def do_create(self, class_name: str):
        """create <class_name>:
        Create and saves a new instance of <class_name>"""
        # Verify class name
        if not self._is_line_valid(class_name, "create"):
            return
        # This looks ridiculous, mb: looks fine lol
        obj = valid_classes[class_name]()
        storage.save()
        print(obj.id)

    def do_show(self, line: str, **kwargs):
        """show class_name object_id: prints the string representation of
        object with id object_id"""
        # Verify argument
        if not kwargs and not self._is_line_valid(line, "show"):
            return
        if kwargs:
            if not self._is_id_kwargs(kwargs):
                return
            class_name = kwargs["class_name"]
            ins_id = self._get_id(kwargs)
        else:
            args = line.split()
            class_name = args[0]
            ins_id = args[1]
        obj_name = f"{class_name}.{ins_id}"
        all_objs = storage.all()
        if obj_name not in all_objs:
            print("** no instance found **")
            return

        # instance exist, print it!
        print(all_objs[obj_name])

    def do_destroy(self, line: str, **kwargs):
        """destroy class_name object_id: destroy the object with the id
        object_id"""
        # Verify argument
        if not kwargs and not self._is_line_valid(line, "destroy"):
            return
        elif kwargs and not self._is_id_kwargs(kwargs):
            return
        if line:
            args = line.split()
            obj_name = f"{args[0]}.{args[1]}"
        else:
            obj_name = f"{kwargs['class_name']}.{self._get_id(kwargs)}"
        all_objs = storage.all()
        if obj_name not in all_objs:
            print("** no instance found **")
            return
        # instance exist, destroy it!
        del all_objs[obj_name]
        storage.save()

    def do_all(self, line: str, **kwargs):
        """all [class_name]: Prints all the current saved objects."""
        if not kwargs and not self._is_line_valid(line, "all"):
            return
        if kwargs:
            line = kwargs["class_name"]
        all_objs = storage.all()
        filter = True if line and line in valid_classes else False
        list_objs = []
        if filter:
            list_objs = [str(v) for k, v in all_objs.items() if line in k]
        else:
            list_objs = [str(v) for _, v in all_objs.items()]
        # do we print an empty list?
        print(list_objs)

    def do_update(self, line: str, **kwargs):
        """update class_name object_id attribute value: Updates the object with
        the id object_id by assigning the attribute <attribute> to <value>"""
        if not self._is_upd_args_valid(line, kwargs):
            return
        if line:
            args = line.split(" ", 3)
            obj_name = f"{args[0]}.{args[1]}"
            self._set_attr(args[2], args[3], obj_name)
            return
        all_objs = storage.all()
        if isinstance(kwargs["options"][1], str):
            options = kwargs["options"]
            obj_name = f"{kwargs['class_name']}.{self._get_id(kwargs)}"
            setattr(all_objs[obj_name], options[1], options[2])
            return

        obj_name = f"{kwargs['class_name']}.{self._get_id(kwargs)}"
        for key, value in kwargs["options"][1].items():
            setattr(all_objs[obj_name], key, value)

    def do_User(self, line):
        """User.command(options): Performs command on User with options"""
        self._call_command("User", line)

    def do_BaseModel(self, line):
        """BaseModel.command(options): Performs command on BaseModel with
        options"""
        self._call_command("BaseModel", line)

    def do_Place(self, line):
        """Place.command(options): Performs command on Place with options"""
        self._call_command("Place", line)

    def do_City(self, line):
        """City.command(options): Performs command on City with options"""
        self._call_command("City", line)

    def do_Review(self, line):
        """Review.command(options): Performs command on Review with options"""
        self._call_command("Review", line)

    def do_Amenity(self, line):
        """Amenity.command(options): Performs command on Amenity with
        options"""
        self._call_command("Amenity", line)

    def do_State(self, line):
        """State.command(options): Performs command on State with options"""
        self._call_command("State", line)

    def _count(self, line, **kwargs):
        """Not a command!
        Counts the number of instances of a class currently stored
        called using the _call_command.
        Parameters:
        - line: Not used
        - kwargs: dictionary with:
            - class_name: name of class to use
            - options: not used
        """
        class_name = kwargs["class_name"]

        # count then print
        all_objs = storage.all()
        count = 0
        for obj_name in all_objs:
            if obj_name.startswith(class_name):
                count += 1

        print(count)

    def _call_command(self, class_name: str, line: str):
        """Calls the right command to perform the task
        Parameters:
        - class_name: name of class to use
        - line: line of text to process.
            text is in the form `.command(options)`
        """
        # moving this from preloop, preloop might not run before onecmd()?
        # onecmd is necessary for testing
        self.valid_commands = {
            "all": self.do_all,
            "count": self._count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
        }
        if not line or line[0] != ".":
            print(f"*** Unknown syntax: {class_name}{line}")
            return
        elif "(" not in line or ")" not in line:
            print(f"*** Unknown syntax: {class_name}{line}")
            return

        line = line[1:]  # removing the first . sign
        parts = line.partition("(")
        command = parts[0]
        options = parts[1] + parts[2]
        del parts  # just felt like
        if command not in self.valid_commands:
            print(f"*** Unknown syntax: {class_name}.{line}")
            return
        try:
            # catch invalid options
            options: tuple = literal_eval(options)
        except (SyntaxError, ValueError):
            # arfs6: chat gpt suggested catching SecurityError but it doesn't
            # workAs. Python can't find it
            print(f"*** Unknown syntax: {class_name}.{line}")
            return
        self.valid_commands[command](None,
                                     class_name=class_name, options=options)

    def _get_update_str(self, line: str):
        """Return the right string to use as value for the update command"""
        # lets make a wild assumption
        if line[0] == '"' and line[-1] == '"':
            return line[1:-1]
        if line[0] == "'" and line[-1] == "'":
            return line[1:-1]
        return line

    def _get_id(self, kwargs):
        """Returns id in kwargs"""
        if isinstance(kwargs["options"], tuple):
            return kwargs["options"][0]
        else:
            return kwargs["options"]

    def _is_line_valid(self, line: str, func: str):
        """validator for all handlers"""
        if not line:
            if func == "all":
                return True
            print("** class name missing **")
            return False
        args = line.split(" ", 3)
        # classname
        if args[0] not in valid_classes:
            print("** class doesn't exist **")
            return False
        if func in ["all", "create"]:
            return True
        arg_l = len(args)
        # instance
        if arg_l == 1:
            print("** instance id missing **")
            return False
        if func in ["destroy", "show"]:
            return True
        # update checks
        args = line.split(" ", 3)
        obj_name = f"{args[0]}.{args[1]}"
        if obj_name not in storage.all():
            print("** no instance found **")
            return False
        if arg_l == 2:  # no attributes
            print("** attribute name missing **")
            return False
        if arg_l == 3:
            print("** value missing **")
            return False
        return True  # All checks passed -- success

    def _is_id_kwargs(self, kwargs):
        """Checks if the options passed is a valid id
        Parameter:
        - kwargs: dictionary containing the options tuple.
        Returns:
        - True: id is valid
        - False: id is not valie
        """
        ins_id = kwargs["options"]
        if not ins_id:
            print("** instance id missing **")
            return False
        # literal_eval can let other type pass and functions expect strings
        # (obj) == obj
        if isinstance(ins_id, str):
            return True
        if not isinstance(ins_id, tuple):
            print("** no instance found **")
            return False
        # (obj, obj) == tuple
        ins_id = ins_id[0]
        if not isinstance(ins_id, str):
            # literal_eval can let other type pass and functions expect strings
            print("** no instance found **")
            return False

        return True

    def _is_upd_args_valid(self, line, kwargs):
        """Validates the parameters of update"""
        all_objs = storage.all()
        if not kwargs:
            if not self._is_line_valid(line, "update"):
                return False
            return True

        if not self._is_id_kwargs(kwargs):
            return False
        obj_name = f"{kwargs['class_name']}.{self._get_id(kwargs)}"
        if obj_name not in all_objs:
            print("** no instance found **")
            return False

        # check for attribute name and value
        arg_l = len(kwargs["options"])
        options = kwargs["options"]
        if not isinstance(options, tuple):  # only one options.
            print("** attribute name missing **")
            return False
        elif not isinstance(options[1], dict) and arg_l == 2:
            print("** value missing **")
            return False
        return True  # all checks passed -- success

    def _set_attr(self, key, val, obj_name):
        """Set the attribute of the object
        Parameters:
        - key: attribute name
        - val: value to set to attribute
        - obj_name: <class_name>.<id> of the object.
        """
        value = None
        try:
            value = float(val) if "." in val else int(val)
        except ValueError as e:
            # just pass value?
            value = self._get_update_str(val)
        all_objs = storage.all()
        instance = all_objs[obj_name]
        setattr(instance, key, value)
        instance.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
