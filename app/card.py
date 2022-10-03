from dataclasses import dataclass
from typing import Literal
import config


@dataclass(order=True)
class Card:
    """
    Dataclass representing a Card, with it's associated attributes
    Order = True enables the sorting Cards in a list - used for test cases to check
    that list of Cards are the same
    The visual shorthand is the sign (e.g. J2) that represents the card visually on the board
    """
    tree_type: Literal[config.TREES]  # Is either a card tree or None
    tree_val: int

    def __post_init__(self):
        if self.tree_type is None or self.tree_val is None:
            self.card_name = None
            self.visual_shorthand = None
        else:
            # TODO - refactor to call it name as opposed to card_name
            self.card_name = f"{self.tree_type} {self.tree_val}"
            self.visual_shorthand = config.CARD_SHORTHANDS[self.card_name]
