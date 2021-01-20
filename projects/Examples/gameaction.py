""" This module implements the GameAction class """
from dice import Dice
from base import Base


class GameAction(Base):
    """
    Every GameActor has, at any given time, a list of possible actions
    from which they can choose.  Some of these possibilities may be
    intrinsic in the actor, while others are made possible by GameObjects
    (e.g. a weapon), by other actors (e.g. interaction) or a GameContext
    (e.g. searching a room).

    A GameAction is an action possibility that has been associated with
    a GameActor.  It has attributes that describe and quantify its effects.
    When the GameAction's C{act()} method is called, it computes probabilities
    and strengths (based on attributes of the actor and enabling artifact)
    and calls the target's C{accept_action()} handler, which will determine
    and return the results.

    @ivar attributes: (dict) of <name,value> pairs
    @ivar source: (GameObject) that delivers this action
    @ivar verb: (string) simple or sub-classed name(s)

    verbs may be simple or sub-classed (with subtypes):
        -   SEARCH
        -   VERBAL.INTIMMIDATE
        -   ATTACK.STAB

    attributes set by client:
        - ATTACK verbs are expected to have ACCURACY (to-hit percentage) and
          DAMAGE (dice formula) attributes.
        - non-ATTACK verbs are expected to have POWER (to-hit percentage) and
          STACKS (number of instances to attempt/deliver) attributes.

    A verb can also be a plus-separated concatenation of simple and/or
    sub-classed verbs.  If a passed verb contains multiple (plus-separated)
    terms, the ACCURACY, DAMAGE, POWER, and STACKS attributes are each assumed
    to be comma-separated lists with the same number of terms.

    Example:
        - verb="ATTACK.STAB+ATTACK.POISON"
        - ACCURACY=60,40
        - DAMAGE=D6,3D4
    """
    def __init__(self, source, verb):
        """
        create a new C{GameAction}
        @param source: (GameObject) instrument for the action
        @param verb: (string) the name of the action
        """
        super(GameAction, self).__init__(verb)
        self.source = source
        self.verb = verb
        self.attributes = {}

    def __str__(self):
        """
        return a string representation of our verb and key attributes
        """
        if "ATTACK" in self.verb:
            return "{} (ACCURACY={}%, DAMAGE={})".\
                format(self.verb, self.get("ACCURACY"), self.get("DAMAGE"))
        return "{} (POWER={}%, STACKS={})".\
            format(self.verb, self.get("POWER"), self.get("STACKS"))

    def act(self, initiator, target, context):
        """
        Initiate an action against a target

        If the verb is a concatenation (list of simple/sub-classed verbs),
        split it and process each action separately.

        This (base-class) C{act()} method knows how to process
        (a list of) simple or sub-typed verbs that are simply a
        matter of looking up initiator bonus values,
        adding them up, and calling the target's C{accept_action()}
        handler, passing:
            - the C{GameAction} (with all of its attributes)
            - the initiating C{GameActor}
            - the C{GameContext} in which this is taking place

        When the target is called, the C{GameAction} attributes will
        include (for ATTACK verbs):
            - C{TO_HIT}: 100 + sum of action's and actor's C{ACCURACY}
            - C{DAMAGE}: sum of rolls against actions's and actor's C{DAMAGE}
        for non-attack verbs:
            - C{TO_HIT}: 100 + the action's and initiator's C{POWER}
            - C{STACKS}: sum of rolls against actions's and initiator's C{STACKS}

        Actions that require more complex processing (before
        calling the target) must be implemented (by additional
        code in a sub-class that extends this method (at least
        for the verbs in question)

        @param initiator: (GameActor) initiating the action
        @param target: (GameObject) target of the action
        @param context: (GameContext) in which this is happening
        @return: (string) description of the results (returned from the target)

        """
        # if the verb is a concatenation
        #   split verb into a list of individual plus-separated (simple or sub-typed) verbs
        #   get_list split the ACCURACY, DAMAGE, POWER and STACKS into a corresponding lists
        #
        # for each verb in the list
        #   if ATTACK
        #       self.TO_HIT= 100 + self.accuracy(verb, ACCURACY, initiator)
        #       self.HIT_POINTS= self.damage(verb, DAMAGE, initiator)
        #   else
        #       self.TO_HIT= 100 + self.power(verb, POWER, initiator)
        #       self.TOTAL= self.stacks(verb, STACKS, initiator)
        #   (success, result) target.accept_action(self, initiator, context)
        #       and accumulate the results
        return (True, "FIXME")

    #
    # the following methods are all private helpers, used by act
    #
    def accuracy(self, verb, base, initiator):
        """
        Compute the accuracy of this attack ... based on the supplied
        base and any initiator ACCURACY(.subtype) bonus.

        @param verb: (string) attack verb
        @param base: (int) accuracy (from the action)
        @param initiator: (GameActor) who is initiating the attack
        @return: (int) probability of hitting
        """
        # start with the specified base accuracy
        # if initiator has an ACCURACY.subtype, add that
        return 0

    def damage(self, verb, base, initiator):
        """
        compute the damage resulting from this attack
        @param verb: (string) attack verb
        @param base: (string) dice formula for base damage
        @param initiator: (GameActor) who is initiating the attack
        @return: (int) total damage
        """
        # roll the specified base damage formula
        # roll the initiator's base DAMAGE formula and add it
        # if the initiator has a DAMAGE.subtype, roll and add it
        return 0

    def power(self, verb, base, initiator):
        """
        Compute the power with which this condition is being sent
        @param verb: (string) action verb
        @param base: (int) base power (from action)
        @param initiator: (GameActor) who is sending the condition
        @return: (int) total probability of hitting
        """
        # start with the specified base power
        # add the initiator's POWER.base_verb
        # add the initiator's POWER.base_verb.subtype
        return 0

    def stacks(self, verb, base, initiator):
        """
        Compute the number of stacks to be sent
        @param verb: (string) action verb
        @param base: (string) dice formulat for base stacks
        @param initiator: (GameActor) who is sending the condition
        @return: (int) total number of stacks
        """
        # roll the specified base # stacks (default 1)
        # roll add the initiator's STACKS.base_verb formula and add it
        # roll initiator's STACKS.base_verb.subtype formula and add it
        return 0

    def get_list(self, name, size):
        """
        read the specified attribute and lex its (comma-separated) values into a list
        @param name: (string) name of attribute to be looked up and split
        @param size: (int) length of desired list
        @return: (list of strings)
            - if no value is found, a list of Nones will be returned
            - if there is only single value, it will be replicated the specified number of times
        """
        return [None] * size
