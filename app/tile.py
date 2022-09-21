from dataclasses import dataclass, field
from typing import Literal
import config


@dataclass()
class Tile:
    card_tree: Literal[config.TREES]  # Is either a card tree or None
    card_num: int

    def __post_init__(self):
        if self.card_tree is None or self.card_num is None:
            self.card_name = None
            self.visual_shorthand = None
        else:
            self.card_name = f"{self.card_tree} {self.card_num}"
            self.visual_shorthand = config.CARD_SHORTHANDS[self.card_name]

if __name__ == "__main__":
    tile = Tile(card_tree="Oak", card_num=2)
    print("AAA")
