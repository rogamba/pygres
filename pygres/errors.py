#-*- coding: utf-8 -*-
class PygresError(Exception):
    """Exception raised for errors in the input.
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
