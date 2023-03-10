#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Test case for the Console.
"""
import os
import unittest
import io
from unittest.mock import patch
from console import HBNBCommand
from models import storage


class TestConsole(unittest.TestCase):
    """Test case for TestConsole attributes"""

    def setUp(self):
        """setup"""
        self.id_regex = r"[\d\w]{8}-[\d\w]{4}-[\d\w]{4}-[\d\w]{4}-[\d\w]{12}"
        storage.fpa = "test_console_db.json"
        if (os.path.isfile(storage.fpa)):
            os.remove(storage.fpa)
        storage.reload()
        self.storage = storage

    def tearDown(self):
        """ teardown """
        if (os.path.isfile(self.storage.fpa)):
            os.remove(self.storage.fpa)
        del self.storage

    def test_help_all(self):
        """Tesing `help all` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("help all")
            self.assertEqual(
                HBNBCommand.do_all.__doc__ + "\n", f.getvalue())
            f.close()

    def test_help_show(self):
        """Tesing `help show` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("help show")
            self.assertEqual(
                HBNBCommand.do_show.__doc__ + "\n", f.getvalue())
            f.close()

    def test_help_update(self):
        """Tesing `help update` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("help update")
            self.assertEqual(
                HBNBCommand.do_update.__doc__ + "\n", f.getvalue())
            f.close()

    def test_help_destroy(self):
        """Tesing `help destroy` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("help destroy")
            self.assertEqual(
                HBNBCommand.do_destroy.__doc__ + "\n", f.getvalue())
            f.close()

    def test_quit(self):
        """Tesing `quit` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            ret = HBNBCommand().onecmd("quit")
            self.assertEqual(ret, True)
            f.close()

    def test_eof(self):
        """Tesing `EOF ctrl-D` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("EOF")
            self.assertEqual("\n", f.getvalue())
            f.close()

    def test_emptyline(self):
        """Tesing `emptyline` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("\n")
            self.assertEqual("", f.getvalue())
            f.close()

    def test_help_create(self):
        """Tesing `help create` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("help create")
            self.assertEqual(
                HBNBCommand.do_create.__doc__ + "\n", f.getvalue())
            f.close()

    def test_create_invalid(self):
        """testing invalid create command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create")
            self.assertEqual("** class name missing **\n", f.getvalue())
            f.close()

    def test_create_invalid_arg(self):
        """testing invalid create command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create invalid")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
            f.close()

    def test_create_valid_basemodel(self):
        """testing valid create BaseModel command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            self.assertRegex(
                f.getvalue(),
                self.id_regex)
            f.close()

    def test_create_valid_user(self):
        """testing valid create user command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create User")
            self.assertRegex(
                f.getvalue(),
                self.id_regex)
            f.close()

    def test_create_valid_amenity(self):
        """testing valid create Amenity command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create Amenity")
            self.assertRegex(
                f.getvalue(),
                self.id_regex)
            f.close()

    def test_create_valid_city(self):
        """testing valid create City command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create City")
            self.assertRegex(
                f.getvalue(),
                self.id_regex)
            f.close()

    def test_create_valid_place(self):
        """testing valid create Place command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create Place")
            self.assertRegex(
                f.getvalue(),
                self.id_regex)
            f.close()

    def test_create_valid_state(self):
        """testing valid create State command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create State")
            self.assertRegex(
                f.getvalue(),
                self.id_regex)
            f.close()

    def test_create_valid_review(self):
        """testing valid create Review command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("create Review")
            self.assertRegex(
                f.getvalue(),
                self.id_regex)
            f.close()

    def test_destroy_basemodel_invalid(self):
        """testing `destroy BaseModel` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_destroy_basemodel_function_invalid(self):
        """testing `BaseModel.destroy()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_destroy_place_function_invalid(self):
        """testing `Place.destroy()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Place.destroy()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_destroy_user_function_invalid(self):
        """testing `User.destroy()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("User.destroy()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_destroy_amenity_function_invalid(self):
        """testing `Amenity.destroy()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Amenity.destroy()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_destroy_city_function_invalid(self):
        """testing `City.destroy()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("City.destroy()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_destroy_state_function_invalid(self):
        """testing `State.destroy()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("State.destroy()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_destroy_review_function_invalid(self):
        """testing `Review.destroy()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Review.destroy()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_update_basemodel_invalid(self):
        """testing `update BaseModel` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_update_basemodel_function_invalid(self):
        """testing `BaseModel.update()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_update_place_function_invalid(self):
        """testing `Place.update()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Place.update()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_update_user_function_invalid(self):
        """testing `User.update()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("User.update()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_update_amenity_function_invalid(self):
        """testing `Amenity.update()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Amenity.update()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_update_city_function_invalid(self):
        """testing `City.update()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("City.update()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_update_state_function_invalid(self):
        """testing `State.update()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("State.update()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_update_review_function_invalid(self):
        """testing `Review.update()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Review.update()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_all_basemodel(self):
        """testing `all BaseModel` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("all BaseModel")
            self.assertEqual("[]\n", f.getvalue())
            f.close()

    def test_all_basemodel_function(self):
        """testing `BaseModel.all()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.all()")
            self.assertEqual("[]\n", f.getvalue())
            f.close()

    def test_all_place_function(self):
        """testing `Place.all()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Place.all()")
            self.assertEqual("[]\n", f.getvalue())
            f.close()

    def test_all_user_function(self):
        """testing `User.all()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("User.all()")
            self.assertEqual("[]\n", f.getvalue())
            f.close()

    def test_all_amenity_function(self):
        """testing `Amenity.all()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Amenity.all()")
            self.assertEqual("[]\n", f.getvalue())
            f.close()

    def test_all_city_function(self):
        """testing `City.all()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("City.all()")
            self.assertEqual("[]\n", f.getvalue())
            f.close()

    def test_all_state_function(self):
        """testing `State.all()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("State.all()")
            self.assertEqual("[]\n", f.getvalue())
            f.close()

    def test_all_review_function(self):
        """testing `Review.all()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Review.all()")
            self.assertEqual("[]\n", f.getvalue())
            f.close()

    def test_count_basemodel_function(self):
        """testing `BaseModel.count()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.count()")
            self.assertEqual("0\n", f.getvalue())
            f.close()

    def test_count_place_function(self):
        """testing `Place.count()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Place.count()")
            self.assertEqual("0\n", f.getvalue())
            f.close()

    def test_count_user_function(self):
        """testing `User.count()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("User.count()")
            self.assertEqual("0\n", f.getvalue())
            f.close()

    def test_count_amenity_function(self):
        """testing `Amenity.count()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Amenity.count()")
            self.assertEqual("0\n", f.getvalue())
            f.close()

    def test_count_city_function(self):
        """testing `City.count()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("City.count()")
            self.assertEqual("0\n", f.getvalue())
            f.close()

    def test_count_state_function(self):
        """testing `State.count()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())
            f.close()

    def test_count_review_function(self):
        """testing `Review.count()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Review.count()")
            self.assertEqual("0\n", f.getvalue())
            f.close()

    def test_show_invalid(self):
        """testing invalid show command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("show")
            self.assertEqual("** class name missing **\n", f.getvalue())
            f.close()

    def test_show_bad_class(self):
        """testing show bad class command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("show BadClass")
            self.assertEqual("** class doesn't exist **\n", f.getvalue())
            f.close()

    def test_show_missing_id(self):
        """testing show missing id command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_show_basemodel_function_invalid(self):
        """testing `BaseModel.show()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_show_place_function_invalid(self):
        """testing `Place.show()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Place.show()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_show_user_function_invalid(self):
        """testing `User.show()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("User.show()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_show_amenity_function_invalid(self):
        """testing `Amenity.show()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Amenity.show()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_show_city_function_invalid(self):
        """testing `City.show()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("City.show()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_show_state_function_invalid(self):
        """testing `State.show()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("State.show()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()

    def test_show_review_function_invalid(self):
        """testing `Review.show()` command"""
        with patch('sys.stdout', new=io.StringIO()) as f:
            HBNBCommand().onecmd("Review.show()")
            self.assertEqual("** instance id missing **\n", f.getvalue())
            f.close()
