#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Includes the class BaseModel which is the base of each class.
"""
from uuid import uuid4
from datetime import datetime
from . import storage


class BaseModel:
    """Defines common attributes and methods for all other classes"""

    def __init__(self, *args, **kwargs):
        """Initialize all the attributes of the object"""
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
            return

        # Create attributes from kwargs
        ignore = ('__class__', 'created_at', 'updated_at')
        self.created_at = datetime.fromisoformat(
            self.val_str_or_raise('created_at', kwargs['created_at'])
        )
        self.updated_at = datetime.fromisoformat(
            self.val_str_or_raise('updated_at', kwargs['updated_at'])
        )

        for attr, value in kwargs.items():
            if attr not in ignore:
                setattr(self, attr, value)

    def __str__(self):
        """Returns a string representation of the object"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def val_str_or_raise(self, name, string):
        """ validate string or raise """
        if not isinstance(string, str):
            raise TypeError(f"{name} must be a string")
        if not string:
            raise ValueError(f"{name} can't be empty")
        return string

    def save(self):
        """Update the updated_at attribute"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all the attributes of the object"""
        attrs = self.__dict__.copy()
        attrs['__class__'] = self.__class__.__name__
        attrs['created_at'] = self.created_at.isoformat()
        attrs['updated_at'] = self.updated_at.isoformat()
        return attrs
