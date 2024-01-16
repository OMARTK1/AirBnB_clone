#!/usr/bin/python3
"""It defines the Review class"""
from models.base_model import BaseModel


class Review(BaseModel):
    """It is representing a review

    Attributes:
        place_id (str): The Place id
        user_id (str): The User id
        text (str): The text of the review
    """

    place_id = ""
    user_id = ""
    text = ""
