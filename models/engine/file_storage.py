#!/usr/bin/python3
""" its a module defining the file_storage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """a class that represent an abstracted storage engine.

    attribute:
        __file_paths (str): represent the name of
                            the file to save objects on it
        __objects (dict): it's dictionary of instantiated  object
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """it return the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """it set in "__objects" obj with the key <obj_class_name>.id"""
        oc_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(oc_name, obj.id)] = obj

    def save(self):
        """it serialize the "__objects" to JSONfile __file_path."""
        ob_dict = FileStorage.__objects
        obj_dict = {obj: ob_dict[obj].to_dict() for obj in ob_dict.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """it deserialize JSONfile "__file_path"
            to "__objects", if existing
        """
        try:
            with open(FileStorage.__file_path) as f:
                objdict = json.load(f)
                for o in objdict.values():
                    c_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(c_name)(**o))
        except FileNotFoundError:
            return
