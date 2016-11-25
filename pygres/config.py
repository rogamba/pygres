# -*- coding: utf-8 -*-
import os

class Config(dict):
    """
    Works like a dict
    """
    def from_object(self, obj):
        """Updates the values from the given object.  An object can be of one
        of the following two types:
        """
        if isinstance(obj, string_types):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
