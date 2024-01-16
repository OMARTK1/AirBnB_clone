#!/usr/bin/python3
"""Defines unittests for models/review.py

Unittest classes:
    TestReview_instantiation
    TestReview_to_dict
    TestReview_save
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_instantiation(unittest.TestCase):
    """The unittests for testing instantiation of the Review class"""

    def test_no_args_instantiates(self):
        """It tests that Review instantiation without arguments works"""
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        """It tests that a new Review instance is stored in the storage"""
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        """It tests that Review's id attribute is a public string"""
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        """It tests that Review's created_at attribute is a public datetime"""
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        """It tests that Review's updated_at attribute is a public datetime"""
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        """It tests that Review's place_id is a public class attribute"""
        rv = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(rv))
        self.assertNotIn("place_id", rv.__dict__)

    def test_user_id_is_public_class_attribute(self):
        """It tests that Review's user_id is a public class attribute"""
        rv = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(rv))
        self.assertNotIn("user_id", rv.__dict__)

    def test_text_is_public_class_attribute(self):
        """It tests that Review's text is a public class attribute"""
        rv = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(rv))
        self.assertNotIn("text", rv.__dict__)

    def test_two_reviews_unique_ids(self):
        """It tests that two Review instances have unique ids"""
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.id, rv2.id)

    def test_two_reviews_different_created_at(self):
        """It tests that two Review instances have different created_at"""
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.created_at, rv2.created_at)

    def test_two_reviews_different_updated_at(self):
        """It tests that two Review instances have different updated_at"""
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.updated_at, rv2.updated_at)

    def test_str_representation(self):
        """It tests the string representation of the Review instance"""
        dt = datetime.today()
        dt_repr = repr(dt)
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        rvstr = rv.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + dt_repr, rvstr)
        self.assertIn("'updated_at': " + dt_repr, rvstr)

    def test_args_unused(self):
        """It tests that Review instantiation with unused args
        doesn't add them"""
        rv = Review(None)
        self.assertNotIn(None, rv.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """It tests that Review instantiation with kwargs sets attributes"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        rv = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(rv.id, "345")
        self.assertEqual(rv.created_at, dt)
        self.assertEqual(rv.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """It tests that instantiation with None kwargs raises TypeError"""
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """The unittests for testing save method of the Review class"""

    @classmethod
    def setUp(self):
        """It sets up method to handle file operations before tests"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """It tears down method to handle file operations after tests"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """It tests that calling save() updates the 'updated_at' attribute"""
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        self.assertLess(first_updated_at, rv.updated_at)

    def test_two_saves(self):
        """It tests that calling save() twice updates 'updated_at'
        accordingly"""
        rv = Review()
        sleep(0.05)
        first_updated_at = rv.updated_at
        rv.save()
        second_updated_at = rv.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        rv.save()
        self.assertLess(second_updated_at, rv.updated_at)

    def test_save_with_arg(self):
        """It tests that calling save() with an argument raises TypeError"""
        rv = Review()
        with self.assertRaises(TypeError):
            rv.save(None)

    def test_save_updates_file(self):
        """It tests that the save method updates the file"""
        rv = Review()
        rv.save()
        rvid = "Review." + rv.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


class TestReview_to_dict(unittest.TestCase):
    """The unittests for testing to_dict method of the Review class"""

    def test_to_dict_type(self):
        """It tests that the result of to_dict is of type dict"""
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """It tests that to_dict contains the expected keys"""
        rv = Review()
        self.assertIn("id", rv.to_dict())
        self.assertIn("created_at", rv.to_dict())
        self.assertIn("updated_at", rv.to_dict())
        self.assertIn("__class__", rv.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """It tests that to_dict() includes dynamically added attributes"""
        rv = Review()
        rv.middle_name = "Holberton"
        rv.my_number = 98
        self.assertEqual("Holberton", rv.middle_name)
        self.assertIn("my_number", rv.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """It tests that the datetime attributes in to_dict() are strings"""
        rv = Review()
        rv_dict = rv.to_dict()
        self.assertEqual(str, type(rv_dict["id"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["updated_at"]))

    def test_to_dict_output(self):
        """It tests the correctness of the to_dict() output"""
        dt = datetime.today()
        rv = Review()
        rv.id = "123456"
        rv.created_at = rv.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(rv.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """It tests that to_dict() is different from the __dict__ attribute"""
        rv = Review()
        self.assertNotEqual(rv.to_dict(), rv.__dict__)

    def test_to_dict_with_arg(self):
        """It tests that calling to_dict with an argument raises a TypeError"""
        rv = Review()
        with self.assertRaises(TypeError):
            rv.to_dict(None)


if __name__ == "__main__":
    unittest.main()
