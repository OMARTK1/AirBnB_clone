#!/usr/bin/python3
"""The initialization of the models package"""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
