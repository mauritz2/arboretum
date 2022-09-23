from dataclasses import dataclass
from typing import Literal
import config


@dataclass()
class Card:
    tree_type: Literal[config.TREES]  # Is either a card tree or None
    tree_val: int

    def __post_init__(self):
        if self.tree_type is None or self.tree_val is None:
            self.card_name = None
            self.visual_shorthand = None
        else:
            self.card_name = f"{self.tree_type} {self.tree_val}"
            self.visual_shorthand = config.CARD_SHORTHANDS[self.card_name]