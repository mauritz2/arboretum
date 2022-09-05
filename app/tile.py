from dataclasses import dataclass
from typing import Literal
import config


@dataclass
class Tile:
    # TBD - this class should be used since it's better than keeping track of strings in a list
    card_tree: Literal[config.TREES]  # Is either a card tree or None
    card_num: int
    x_coord: int
    y_coord: int
    card_name = f"{card_tree} {card_num}"
    visual_sign: str = config.DECK_SHORTHANDS[card_name]