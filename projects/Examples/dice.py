"""
This module provides the Dice class (formula based random numbers)
"""
import sys
from random import randint


class Dice(object):
    """
    This class supports formula based dice rolls.
    The formulae can be described in a few (fairly standard) formats:
        - DnD style ... D100, 3D6, 3D6+4
        - ranges ... 4-12
        - simple numbers ... 50

    @ivar num_dice: (int) number of dice to be rolled, None if a range
    @ivar dice_type: (int) number of faces on each die, None if a range
    @ivar plus: (int) number to be added to the roll
    @ivar min_value: (int) lowest legal value in range, None if a formula
    @ivar max_value: (int) highest legal value range, None if a formula

    """

    def __init__(self, formula):
        """
        instantiate a roller for a specified formula

        @param formula: (string) description of roll
        @raise ValueError: illegal formula expression
        """
        # recognize integer formula as plus value
        # recognize simple numeric string as plus value
        # process "#-#" as min and max values
        # process "xDy" or "xDy+z" as num_dice, dice_type and plus
        # if formula is a numeric string, use that as plus value
        # if formula is #-#, use those as min and max values
        # if formula contains a D
        #   leading string is num_dice, default 1
        # if trailing string contains a +
        #   leading number is dice_type
        #   second number is the plus
        # else
        #   number is dice_type

    def __str__(self):
        """
        @return: (string) representation of our formula (#, #-#, #D#+#)
        """
        return "0"

    def roll(self):
        """
        roll this set of dice and return result
        @return: (int) resulting value
        """
        # range: generate a random number between them
        # formula: accumulate num_dice numbers between 1 and dice_type, add plus
        return 0

