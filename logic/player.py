import logic.config as config
from logic.deck import Deck
from logic.board import Board
from logic.graveyard import Graveyard


class Player:
    def __init__(self,
                 name: str,
                 deck: Deck,
                 graveyard: Graveyard,
                 board: Board,
                 num_cards_starting_hand: int = config.NUM_CARDS_STARTING_HAND):

        self.name = name
        self.cards_on_hand = {}
        # TODO - This inheritance doesn't make sense - why would each player have their own Deck?
        # It probably makes more sense to have the deck be owned by the GameManager?
        self.deck = deck
        self.graveyard = graveyard
        self.board = board
        self.first_tree_placed = False
        self.score = 0

        for i in range(num_cards_starting_hand):
            self.draw_card_from_deck()

    def place_tree(self, card_name: str, row: int, column: int) -> None:
        """
        Takes the str of a card name (e.g. Oak 2) and the coordinates to place it
        Checks if valid placement, and if so places card on board and removes from player hand
        Returns ValueError if card isn't in players hand or placement is illegal
        """
        if card_name not in self.cards_on_hand:
            raise ValueError(f"You cannot play card {card_name} you don't have in your hand: {self.cards_on_hand}")

        self.board.check_if_valid_board_location(row, column)

        if self.first_tree_placed:
            if not self.board.check_if_slot_has_adjacent_tree(row, column):
                raise ValueError(f"You cannot place a tree at ({row}, {column}) since it's not adjacent to an existing tree")

        self.board.board_grid[row][column] = self.cards_on_hand[card_name]
        self.discard_card(card_name=card_name, to_graveyard=False)
        self.first_tree_placed = True

    def draw_card_from_deck(self) -> None:
        # TODO - remove inconsistency where card[0] is top card in deck, but bottom card in graveyard
        card = self.deck.cards[0]
        self.cards_on_hand[card.card_name] = card
        self.deck.remove_top_card()

    def draw_card_from_graveyard(self, player_to_draw_from: 'Player') -> None:
        """
        Takes a player as input to determine what player's graveyard to draw from
        Draws a card from that pile (i.e. removes it from that graveyard and adds it to player hand)
        Type hint is 'Player' as a str since from __future__ import annotations was throwing an error
        """
        if len(self.graveyard.cards) <= 0:
            raise ValueError(f"The targeted discard pile of {self.name} is empty. Try drawing from another discard pile or the deck.")
        card = player_to_draw_from.graveyard.get_top_card()
        self.cards_on_hand[card.card_name] = card
        player_to_draw_from.graveyard.remove_top_card()

    def discard_card(self, card_name: str, to_graveyard: bool) -> None:
        if to_graveyard:
            self.graveyard.add_card_on_top(self.cards_on_hand[card_name])
        del self.cards_on_hand[card_name]

    def get_player_card_names(self) -> list[str]:
        """
        Returns the names of all the cards on hand, sorted by tree type
        """
        cards_on_hand = list(self.cards_on_hand.keys())
        cards_on_hand.sort()
        return cards_on_hand
