import config
import random


class Deck:
    def __init__(self, tree_types: list = config.TREES, num_cards_per_type: int = config.CARDS_PER_TREE_TYPE):
        self.cards = self._generate_deck(tree_types, num_cards_per_type)

        self.shuffle_deck()

    def _generate_deck(self, tree_types, num_cards_per_type):
        cards = []
        for tree in tree_types:
            for i in range(num_cards_per_type):
                card_name = f"{tree} {i + 1}"
                cards.append(card_name)
        return cards

    def remove_top_card(self):
        del self.cards[0]

    def shuffle_deck(self):
        random.shuffle(self.cards)
