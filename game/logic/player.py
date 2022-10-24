import game.config as config
from game.logic.deck import Deck
from game.logic.board import Board
from game.logic.discard import Discard


class Player:
    def __init__(self,
                 name: str,
                 deck: Deck,
                 discard: Discard,
                 board: Board,
                 num_cards_starting_hand: int = config.NUM_CARDS_STARTING_HAND):

        self.name = name
        self.cards_on_hand = {}
        self.deck = deck
        self.discard = discard
        self.board = board
        self.first_tree_placed = False
        self.score = 0

        for i in range(num_cards_starting_hand):
            self.draw_card_from_deck()

    def play_card(self, card_name: str, row: int, column: int) -> None:
        """
        Takes the str of a card name (e.g. Oak 2) and the coordinates to place it
        Checks if valid placement, and if so places card on board and removes from player hand
        Returns ValueError if card isn't in players hand or placement is illegal
        """
        if card_name not in self.cards_on_hand:
            raise ValueError(f"You cannot play card {card_name} you don't have in your hand: {self.cards_on_hand}")

        is_valid_board_location, error_msg = self.board.is_valid_board_location(row, column)

        if not is_valid_board_location:
            raise ValueError(error_msg)

        if self.first_tree_placed:
            if len(self.board.get_adjacent_cards(row, column)) == 0:
                raise ValueError(f"You cannot place a tree at ({row}, {column}) since it's not adjacent to an existing tree.")

        self.board.board_grid[row][column] = self.cards_on_hand[card_name]
        self.discard_card(card_name=card_name, to_discard=False)
        self.first_tree_placed = True

    def draw_card_from_deck(self) -> None:
        card = self.deck.get_top_card()
        self.cards_on_hand[card.name] = card
        self.deck.remove_top_card()

    def draw_card_from_discard(self, player_to_draw_from: 'Player') -> None:
        """
        Takes a player as input to determine what player's discard to draw from
        Draws a card from that pile (i.e. removes it from that discard and adds it to player hand)
        Type hint is 'Player' as a str since from __future__ import annotations was throwing an error

        # TODO - refactor so it takes a PLayer name as input as opposed to passing an entire Player instance
        """
        # TODO - would this make more sense if this took a player name as input vs. a player instance?
        # Downside is that it would have to call get_player_instance on the scorer class, which would be odd
        # keeping like this for now
        if len(player_to_draw_from.discard.cards) <= 0:
            raise ValueError(f"The targeted discard pile of {player_to_draw_from.name} is empty. Try drawing from another discard pile or the deck.")
        card = player_to_draw_from.discard.get_top_card(only_str=False)
        self.cards_on_hand[card.name] = card
        player_to_draw_from.discard.remove_top_card()

    def discard_card(self, card_name: str, to_discard: bool) -> None:
        if to_discard:
            self.discard.add_card_on_top(self.cards_on_hand[card_name])
        del self.cards_on_hand[card_name]

    def get_player_card_names(self) -> list[str]:
        """
        Returns the names of all the cards on hand, sorted by tree type
        """
        cards_on_hand = list(self.cards_on_hand.keys())
        cards_on_hand.sort()
        return cards_on_hand
