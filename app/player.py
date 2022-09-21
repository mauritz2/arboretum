import config
from deck import Deck
from board import Board


class Player:
    def __init__(self, name: str, deck: Deck, board: Board,
                 num_cards_starting_hand: int = config.NUM_CARDS_STARTING_HAND):
        # TODO - The GameManager should be able to test for name uniqueness
        self.name = name
        self.trees_on_hand = []
        self.deck = deck
        self.board = board
        self.first_tree_placed = False

        for i in range(num_cards_starting_hand):
            self.draw_card()

    def place_tree(self, tree: str, row: int, column: int):
        if tree not in self.trees_on_hand:
            raise ValueError(f"You cannot play card {tree} you don't have in your hand: {self.trees_on_hand}")

        self.board.check_if_valid_board_location(row, column)

        if self.first_tree_placed:
            if not self.board.check_if_tree_has_adjacent_tree(row, column):
                raise ValueError(f"You cannot place a tree that's not adjacent to an existing tree")

        self.board.board_grid[row][column] = config.CARD_SHORTHANDS[tree]
        self.trees_on_hand.remove(tree)
        self.first_tree_placed = True

    def draw_card(self):
        # TODO - implement drawing from Graveyard
        self.trees_on_hand.append(self.deck.cards[0])
        self.deck.remove_top_card()

    def discard_card(self):
        raise NotImplemented()
