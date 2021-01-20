""" This module implements the base class for almost everything"""


class Base(object):
    """
    This is the base class for all other classes

    @ivar name:         name of this object
    @ivar description:  one line this description
    @ivar attributes:   dict of <name,value> pairs"
    """

    def __init__(self, name, descr=None):
        """
        create a new object
        @param name: display name of this object
        @param descr: human description of this object
        """
        self.name = name
        self.description = descr
        self.attributes = {}

    def __str__(self):
        """
        return a descriptive string for this object
        """
        if self.description is None:
            return self.name
        return "{}({})".format(self.name, self.description)

    def get(self, attribute):
        """
        return: value of an attribute

        @param attribute: name of attribute to be fetched
        @return: (string) value (or none)
        """
        if attribute in self.attributes:
            return self.attributes[attribute]
        return None

    def set(self, attribute, value):
        """
        set the value of an attribute

        @param attribute: name of attribute to be fetched
        @param value: value to be stored for that attribute
        """
        self.attributes[attribute] = value
