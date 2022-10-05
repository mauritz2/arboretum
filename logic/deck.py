import logic.config as config
import random
from logic.card import Card


class Deck:
    def __init__(self,tree_types: list = None, num_cards_per_type: int = config.CARDS_PER_TREE_TYPE):
        tree_types = config.TREES if tree_types is None else tree_types
        self.cards = self._generate_deck(tree_types, num_cards_per_type)
        self.shuffle_deck()

    @staticmethod
    def _generate_deck(tree_types: list[str], num_cards_per_type: int) -> list[Card]:
        cards = []
        # TODO - improve performance by replacing loop with list comprehension
        for tree in tree_types:
            for i in range(num_cards_per_type):
                tree_val = i + 1
                card = Card(tree_type=tree, tree_val=tree_val)
                cards.append(card)
        return cards

    def remove_top_card(self) -> None:
        del self.cards[0]

    def shuffle_deck(self) -> None:
        random.shuffle(self.cards)

    def check_amt_of_cards_left(self) -> int:
        return len(self.cards)

