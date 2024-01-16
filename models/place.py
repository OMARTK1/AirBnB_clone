#!/usr/bin/python3
"""This module defines the Place class"""
from models.base_model import BaseModel


class Place(BaseModel):
    """A class that represent a Place

    attributes:
        city_id (str): represent the City id
        user_id (str): represent the User id
        name (str): represent the name of the place
        description (str): describe the place
        number_rooms (int): represent the nb of rooms of the place
        number_bathrooms (int): the nb of bathrooms of the place
        max_guest (int): The max nb of guests of the place
        price_by_night (int): Price by night of the place
        latitude (float): Width of the place
        longitude (float): Length of the place
        amenity_ids (list): List of Amenity "ids"
    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
