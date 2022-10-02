from dataclasses import dataclass
from card import Card


@dataclass()
class Graveyard:
    """
    Graveyard deck containing discarded cards. The players can draw from either player's graveyard.
    Position 0 in self.cards is the bottom card.
    Position -1 is the last (i.e. top card) that you can draw from.
    """
    cards = list[Card]

    def __len__(self):
        return len(self.cards)

    def get_top_card(self) -> None:
        if len(self.cards):
            raise ValueError("The graveyard is empty")
        return self.cards[-1]

    def remove_top_card(self) -> None:
        del self.cards[-1]

    def add_card_on_top(self, card: Card) -> None:
        self.cards.append(card)








