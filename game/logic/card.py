from typing import Literal
import game.config as config
from dataclasses import dataclass, asdict
from json import dumps


@dataclass(order=True)
class Card:
    """
    Dataclass representing a Card, with it's associated attributes
    tree_type examples: Oak, Cassia, Jacaranda
    tree_num examples: e.g. 1,6,8
    Order = True enables the sorting Cards in a list. This is used for test cases when comparing lists of Cards.
    """
    tree_type: Literal[config.TREES]  # Is either a card tree or None
    tree_num: int

    def __post_init__(self):
        self.name = None if (self.tree_type is None or self.tree_num is None) else f"{self.tree_type} {self.tree_num}"

    @property
    def __dict__(self):
        """
        get a python dictionary
        """
        return asdict(self)

    @property
    def json(self):
        """
        get the json formated string
        """
        return dumps(self.__dict__)


