#!/usr/bin/python3
"""This is the unittests for the models/base_model.py file.

the Unit test classes:
    TestBaseModel->Init
    TestBaseModel->ToDict
    TestBaseModel->Save
"""
import unittest
import models
from models.base_model import BaseModel
import os
from time import sleep
from datetime import datetime


class TestBaseModelInit(unittest.TestCase):
    """Unittests for testing instantiation of the BaseModel class."""

    def test_init_no_args(self):
        """It tests if when we create an instance without arguments it succeed
        """
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        """It tests if there is a new instance
        stored in the "__objects" dict of  storage.
        """
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_init_id_is_public_str(self):
        """it tests if the "id" attribute is a  public str."""
        self.assertEqual(str, type(BaseModel().id))

    def test_init_created_at_is_public_datetime(self):
        """ it tests if the "created_at" attribute
           is  public datetimeObject
        """
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_init_updated_at_is_public_datetime(self):
        """it tests if the "updated_at"
          attribute is  public datetimeObject
        """
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_init_updated_at_is_public_datetime(self):
        """it tests whether 2 models have a unique IDs"""
        bm_1 = BaseModel()
        bm_2 = BaseModel()
        self.assertNotEqual(bm_1.id, bm_2.id)

    def test_init_two_models_unique_ids(self):
        """it tests whether 2 models have
           a different "created_at" time indicators
        """
        bm_1 = BaseModel()
        sleep(0.05)
        bm_2 = BaseModel()
        self.assertLess(bm_1.created_at, bm_2.created_at)

    def test_init_two_models_different_updated_at(self):
        """it tests whether 2 models have a
           different "updated_at" time indicators
        """
        bm_1 = BaseModel()
        sleep(0.05)
        bm_2 = BaseModel()
        self.assertLess(bm_1.updated_at, bm_2.updated_at)

    def test_init_str_representation(self):
        """it tests a string representation
           of the BaseModel
        """
        d_t = datetime.today()
        dt_repr = repr(d_t)
        BM = BaseModel()
        BM.id = "123456"
        BM.created_at = BM.updated_at = d_t
        bmstr = BM.__str__()
        self.assertIn("[BaseModel] (123456)", bmstr)
        self.assertIn("'id': '123456'", bmstr)
        self.assertIn("'created_at': " + dt_repr, bmstr)
        self.assertIn("'updated_at': " + dt_repr, bmstr)

    def test_init_args_unused(self):
        """it tests instantiation
           with the unused  args
        """
        bm = BaseModel(None)
        self.assertNotIn(None, bm.__dict__.values())

    def test_init_with_kwargs(self):
        """it tests instantiation
           with keyword args
        """
        dt = datetime.today()
        dt_iso = dt.isoformat()
        BM = BaseModel(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(BM.id, "345")
        self.assertEqual(BM.created_at, dt)
        self.assertEqual(BM.updated_at, dt)

    def test_init_with_None_kwargs(self):
        """ it tests instantiation with
            "None" keyword args.
        """
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_init_with_args_and_kwargs(self):
        """it tests instantiation
           with both args and keywordArgs
        """
        dt = datetime.today()
        dt_iso = dt.isoformat()
        bm = BaseModel("12", id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(bm.id, "345")
        self.assertEqual(bm.created_at, dt)
        self.assertEqual(bm.updated_at, dt)


class TestBaseModel_to_dict(unittest.TestCase):
    """contain Unittests to test
       "to_dict" method of  BaseModel class
    """

    def test_to_dict_type(self):
        """it tests whether the output
           of "to_dict" is a dictionary
        """
        bm = BaseModel()
        self.assertTrue(dict, type(bm.to_dict()))

    def test_to_dict_correct_keys(self):
        """it tests if the dictionary have correct keys."""
        bm = BaseModel()
        self.assertIn("id", bm.to_dict())
        self.assertIn("created_at", bm.to_dict())
        self.assertIn("updated_at", bm.to_dict())
        self.assertIn("__class__", bm.to_dict())

    def test_to_dict_added_attributes(self):
        """it tests whether the dictionary
           have added attributes
        """
        bm = BaseModel()
        bm.name = "Holberton"
        bm.my_number = 98
        self.assertIn("name", bm.to_dict())
        self.assertIn("my_number", bm.to_dict())

    def test_to_dict_datetime_are_strs(self):
        """it Tests if the "datetime" attributes
               in the dictionary are str
        """
        bm = BaseModel()
        bm_dict = bm.to_dict()
        self.assertEqual(str, type(bm_dict["created_at"]))
        self.assertEqual(str, type(bm_dict["updated_at"]))

    def test_todict_output(self):
        """it tests the output of "to_dict" against another dictionary."""

        dt = datetime.today()
        bm = BaseModel()
        bm.id = "123456"
        bm.created_at = bm.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat()
        }
        self.assertDictEqual(bm.to_dict(), tdict)

    def test_contrast_to_dict_diff_dict(self):
        """it tests what is the difference between "to_dict" & '__dict__.'
        """
        bm = BaseModel()
        self.assertNotEqual(bm.to_dict(), bm.__dict__)

    def test_to_dict_with_args(self):
        """it tests calling "to_dict" with an arg"""
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.to_dict(None)


class TestBaseModel_save(unittest.TestCase):
    """its the Unittests for the save method of  BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_One_save(self):
        """it tests if calling save one time
           updates the "updated_at" time indicators
        """
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        self.assertLess(first_updated_at, bm.updated_at)

    def test_Two_saves(self):
        """it tests if calling save 2 times
           updates "the updated_at" time indicators
        """
        bm = BaseModel()
        sleep(0.05)
        first_updated_at = bm.updated_at
        bm.save()
        second_updated_at = bm.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        bm.save()
        self.assertLess(second_updated_at, bm.updated_at)

    def test_save_with_args(self):
        """it tests calling save with an arg"""
        bm = BaseModel()
        with self.assertRaises(TypeError):
            bm.save(None)

    def test_save_update_file(self):
        """it tests whether calling save
        updates the file and includes the
        instance ID."""
        bm = BaseModel()
        bm.save()
        bmid = "BaseModel." + bm.id
        with open("file.json", "r") as f:
            self.assertIn(bmid, f.read())


if __name__ == "__main__":
    unittest.main()
