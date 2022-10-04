from dataclasses import dataclass
from card import Card


@dataclass()
class Graveyard:
    """
    Graveyard deck containing discarded cards. The players can draw from either player's graveyard.
    Position 0 in self.cards is the bottom card.
    Position -1 is the last (i.e. top card) that you can draw from.
    """
    cards: list[Card]

    def get_top_card(self) -> Card:
        if self.get_amt_of_cards_remaining() <= 0:
            return None
        return self.cards[-1]

    def remove_top_card(self) -> None:
        del self.cards[-1]

    def add_card_on_top(self, card: Card) -> None:
        self.cards.append(card)

    def get_amt_of_cards_remaining(self) -> int:
        return len(self.cards)







