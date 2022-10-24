from dataclasses import dataclass
from game.logic.card import Card


@dataclass()
class Discard:
    """
    The discard pile contains cards discarded by players. The players can draw from either player's discard pile.
    Position 0 in self.cards is the bottom card.
    Position -1 is the last (i.e. top card) that you can draw from.
    """
    cards: list[Card]

    def get_top_card(self, only_str: bool) -> Card:
        """
        Returns the top (i.e. visible) card in the discard pile
        Returns None if the discard pile is empty
        only_str returns the card name (e.g. Oak 1) as a str - implemented to improve information hiding from the UI
        so the UI doesn't get the entire Card class
        """
        if self.get_amt_of_cards_remaining() <= 0:
            return None
        top_card = self.cards[-1]
        if only_str:
            return top_card.name
        else:
            return top_card

    def remove_top_card(self) -> None:
        del self.cards[-1]

    def add_card_on_top(self, card: Card) -> None:
        self.cards.append(card)

    def get_amt_of_cards_remaining(self) -> int:
        return len(self.cards)

    def get_card_names(self) -> list[str]:
        """
        Returns a list of all card names in the discard pile in format: Oak 1
        """
        return self.cards







