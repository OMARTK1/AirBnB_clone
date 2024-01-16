#!/usr/bin/python3
"""It defines the BaseModel class for the AirBnB console project."""
from models import storage
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """it represents the fundamental base class for all project models."""

    def __init__(self, *args, **kwargs):
        """This initialize a new BaseModel instance.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[key] = value
        else:
            storage.new(self)

    def to_dict(self):
        """It returns a dictionary representation of the BaseModel instance.

        Includes the key/value pair '__class__' representing the class name.
        """
        result_dict = self.__dict__.copy()
        result_dict["created_at"] = self.created_at.isoformat()
        result_dict["updated_at"] = self.updated_at.isoformat()
        result_dict["__class__"] = self.__class__.__name__
        return result_dict

    def __str__(self):
        """It returns a string representation of the BaseModel instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """It updates updated_at with the current datetime
        and it saves the instance to storage."""
        self.updated_at = datetime.today()
        storage.save()
