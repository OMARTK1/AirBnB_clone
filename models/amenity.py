#!/usr/bin/python3
"""it's a module defining the amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """A class that represent an amenity.

    Attributes:
        name (str): represent the name of the amenity.
    """
    name = ""
