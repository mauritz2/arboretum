import arboretum.game.config as config
import random
import itertools
from arboretum.game.logic.card import Card


class Deck:
    """
    Class to keep track of the deck with methods to support drawing and getting information about the deck
    Location -1 in the self.cards list indicates the top card that can be drawn
    """
    def __init__(self, tree_types: list = None, num_cards_per_type: int = config.CARDS_PER_TREE_TYPE):
        tree_types = config.TREES if tree_types is None else tree_types
        self.cards = self._generate_deck(tree_types, num_cards_per_type)
        self.shuffle_deck()

    @staticmethod
    def _generate_deck(tree_types: list[str], num_cards_per_type: int) -> list[Card]:
        return [Card(tpl[0], tpl[1]) for tpl in itertools.product(tree_types, range(1, num_cards_per_type + 1))]

    def remove_top_card(self) -> None:
        del self.cards[-1]

    def get_top_card(self) -> Card:
        return self.cards[-1] if self.get_amt_of_cards_left() > 0 else None

    def shuffle_deck(self) -> None:
        random.shuffle(self.cards)

    def get_amt_of_cards_left(self) -> int:
        return len(self.cards)

