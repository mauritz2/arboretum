import config
from deck import Deck
from board import Board


class Player:
    def __init__(self,
                 name: str,
                 deck: Deck,
                 board: Board,
                 num_cards_starting_hand: int = config.NUM_CARDS_STARTING_HAND):

        # TODO - The GameManager should be able to test for name uniqueness
        self.name = name
        self.cards_on_hand = {}
        self.deck = deck
        self.board = board
        self.first_tree_placed = False

        for i in range(num_cards_starting_hand):
            self.draw_card()

    def place_tree(self, card_name: str, row: int, column: int):
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
                raise ValueError(f"You cannot place a tree at ({row}, {column}) \
                 since it's not adjacent to an existing tree")

        self.board.board_grid[row][column] = self.cards_on_hand[card_name]
        self.discard_card(card_name=card_name, to_graveyard=False)
        self.first_tree_placed = True

    def draw_card(self):
        # TODO - implement drawing from Graveyard
        card = self.deck.cards[0]
        self.cards_on_hand[card.card_name] = card
        self.deck.remove_top_card()

    def discard_card(self, card_name: str, to_graveyard: bool):
        # TODO - implement so discarded card appears in Graveyard
        del self.cards_on_hand[card_name]


