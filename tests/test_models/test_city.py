#!/usr/bin/python3
"""It defines the unittests for models/city.py

Unittest classes:
    TestCity_instantiation
    TestCity_to_dict
    TestCity_save
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """The unittests for testing instantiation of the City class"""

    def test_no_args_instantiates(self):
        """It tests that an instance of City is created
        with no arguments"""
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        """It tests that a new instance of City is stored in
        the objects dictionary"""
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        """It test that the 'id' attribute of City is a public string"""
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        """It tests that the 'created_at' attribute of City
        is a public datetime"""
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        """It tests that the 'updated_at' attribute of City
        is a public datetime"""
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        """It tests that 'state_id' is a public class attribute of City"""
        cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cy))
        self.assertNotIn("state_id", cy.__dict__)

    def test_name_is_public_class_attribute(self):
        """It tests that 'name' is a public class attribute of City"""
        cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cy))
        self.assertNotIn("name", cy.__dict__)

    def test_two_cities_unique_ids(self):
        """It tests that two instances of City have unique 'id' values."""
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def test_two_cities_different_created_at(self):
        """It tests that two instances of City have different 'created_at'
        values"""
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def test_two_cities_different_updated_at(self):
        """It tests that two instances of City have different 'updated_at'
        values"""
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def test_str_representation(self):
        """It tests the string representation of City"""
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cystr = cy.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def test_args_unused(self):
        """It tests that passing None as an argument does not affect City
        instance attributes."""
        cy = City(None)
        self.assertNotIn(None, cy.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """It tests instantiation of City with keyword arguments"""
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cy.id, "345")
        self.assertEqual(cy.created_at, dt)
        self.assertEqual(cy.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        """It tests that instantiation of City with None kwargs raises
        a TypeError"""
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """The unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        """It sets up a temporary file before tests"""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """It removes temporary file after tests"""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        """It tests that calling save once updates 'updated_at'"""
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def test_two_saves(self):
        """It tests that calling save twice updates 'updated_at' accordingly"""
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cy.save()
        self.assertLess(second_updated_at, cy.updated_at)

    def test_save_with_arg(self):
        """It tests that calling save with an argument raises a TypeError"""
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def test_save_updates_file(self):
        """It tests that calling save updates the content of the 'file.json'
        file."""
        cy = City()
        cy = City()
        cy.save()
        cyid = "City." + cy.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """The unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        """It tests that the result of to_dict is of type dict"""
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """It tests that to_dict contains the expected keys"""
        cy = City()
        self.assertIn("id", cy.to_dict())
        self.assertIn("created_at", cy.to_dict())
        self.assertIn("updated_at", cy.to_dict())
        self.assertIn("__class__", cy.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """It tests that added attributes are present in to_dict result"""
        cy = City()
        cy.middle_name = "Holberton"
        cy.my_number = 98
        self.assertEqual("Holberton", cy.middle_name)
        self.assertIn("my_number", cy.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        """It tests that datetime attributes in to_dict result are strings"""
        cy = City()
        cy_dict = cy.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        """It tests the correctness of the to_dict output"""
        dt = datetime.today()
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cy.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        """It tests that to_dict result is different from the __dict__
        attribute"""
        cy = City()
        self.assertNotEqual(cy.to_dict(), cy.__dict__)

    def test_to_dict_with_arg(self):
        """It tests that calling to_dict with an argument raises a TypeError"""
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
